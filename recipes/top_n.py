"""Select two sales per store, with a reproducible tie-breaker."""
from pyspark.sql import SparkSession, Window, functions as F


def run(spark):
    sales = spark.sql("""
        SELECT * FROM VALUES
        (1, 'London', 100), (2, 'London', 90), (3, 'London', 90),
        (4, 'Bristol', 50), (5, 'Bristol', 40), (6, 'Bristol', 30)
        AS sales(sale_id, store, amount)
    """)
    order = Window.partitionBy("store").orderBy(
        F.col("amount").desc(), F.col("sale_id").asc()
    )
    top_two = sales.withColumn("position", F.row_number().over(order)).filter(
        F.col("position") <= 2
    )
    top_two.orderBy("store", "position").show()
    assert sorted(r.sale_id for r in top_two.collect()) == [1, 2, 4, 5]

    # Keep all sales tied at the cutoff instead of exactly two rows.
    by_amount = Window.partitionBy("store").orderBy(F.col("amount").desc())
    with_ties = sales.withColumn("rank", F.rank().over(by_amount)).filter(
        F.col("rank") <= 2
    )
    assert sorted(r.sale_id for r in with_ties.collect()) == [1, 2, 3, 4, 5]
    print("PASS: four top-two rows; five rows when cutoff ties are included.")


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[2]").appName("TopNPerGroup").getOrCreate()
    try:
        run(spark)
    finally:
        spark.stop()
