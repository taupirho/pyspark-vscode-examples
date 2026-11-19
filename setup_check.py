"""Run from the example folder with Python 3.13, PySpark 4.2.0 and Java 21."""
from pathlib import Path
import sys

from pyspark.sql import SparkSession


def main():
    print(f"Python: {sys.executable}")
    spark = SparkSession.builder.master("local[2]").appName("SetupCheck").getOrCreate()
    try:
        print(f"Spark version: {spark.version}")
        print(f"Master URL: {spark.sparkContext.master}")
        output = Path(__file__).parent / "output" / "setup_check"
        frame = spark.range(2).selectExpr("id", "'ready' AS status")
        frame.write.mode("overwrite").parquet(output.resolve().as_uri())
        result = spark.read.parquet(output.resolve().as_uri())
        rows_written = result.count()
        assert rows_written == 2, f"Expected 2 rows, got {rows_written}"
        print(f"Rows written: {rows_written}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
