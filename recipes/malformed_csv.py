"""Separate CSV parsing failures from business validation failures."""
from pathlib import Path
from pyspark.sql import SparkSession, functions as F


def run(spark):
    folder = Path(__file__).resolve().parent
    source = (folder / "data" / "sales.csv").as_uri()
    parsed = (
        spark.read.option("header", True)
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .schema("sale_id INT, amount DOUBLE, _corrupt_record STRING")
        .csv(source)
        .cache()
    )
    try:
        assert parsed.count() == 5  # Materialise the full cached input first.
        checked = parsed.withColumn(
            "rejection_reason",
            F.when(F.col("_corrupt_record").isNotNull(), "CSV parse error")
            .when(F.col("sale_id").isNull(), "Missing sale_id")
            .when(F.col("amount").isNull(), "Missing amount")
            .when(F.col("amount") < 0, "Negative amount"),
        )
        rejected = checked.filter(F.col("rejection_reason").isNotNull())
        accepted = checked.filter(F.col("rejection_reason").isNull()).drop(
            "_corrupt_record", "rejection_reason"
        )
        rejected.orderBy("sale_id").show(truncate=False)
        assert sorted(r.sale_id for r in accepted.collect()) == [1, 2]
        assert {r.sale_id: r.rejection_reason for r in rejected.collect()} == {
            3: "CSV parse error", 4: "Missing amount", 5: "Negative amount"
        }
        for name, frame in [("accepted", accepted), ("rejected", rejected)]:
            target = (folder / "output" / "csv_check" / name).as_uri()
            frame.write.mode("overwrite").parquet(target)
        print("PASS: two accepted, three quarantined; output/csv_check written.")
    finally:
        parsed.unpersist()


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[2]").appName("ValidateCsv").getOrCreate()
    try:
        run(spark)
    finally:
        spark.stop()
