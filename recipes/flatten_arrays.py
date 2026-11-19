"""Flatten arrays and preserve aligned elements in two arrays."""
from pyspark.sql import SparkSession, functions as F


def run(spark):
    people = spark.sql("""
        SELECT 'John' AS name, array('apple', 'banana') AS fruits
        UNION ALL SELECT 'Mary', array('orange', 'grape')
        UNION ALL SELECT 'Sam', CAST(array() AS ARRAY<STRING>)
        UNION ALL SELECT 'Alex', CAST(NULL AS ARRAY<STRING>)
    """)
    flat = people.select("name", F.explode("fruits").alias("fruit"))
    flat.orderBy("name", "fruit").show()
    assert flat.count() == 4
    retained = people.select("name", F.explode_outer("fruits").alias("fruit"))
    assert retained.count() == 6
    assert {r.name for r in retained.filter(F.col("fruit").isNull()).collect()} == {"Sam", "Alex"}

    pairs = spark.sql("SELECT array(1, 2, 3) AS numbers, array('a', 'b') AS letters")
    paired = pairs.select(F.explode(F.arrays_zip("numbers", "letters")).alias("pair"))
    result = paired.select("pair.numbers", "pair.letters").orderBy("numbers")
    result.show()
    assert [tuple(r) for r in result.collect()] == [(1, "a"), (2, "b"), (3, None)]
    print("PASS: four exploded rows, six outer rows and three aligned pairs.")


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[2]").appName("FlattenArrays").getOrCreate()
    try:
        run(spark)
    finally:
        spark.stop()
