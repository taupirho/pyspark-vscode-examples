# Three practical PySpark recipes

Companions to the free tutorials at https://profitabledonkeys.com. These examples target Python 3.13, Java 21 and PySpark 4.2.0. Each script asserts its expected results and stops Spark when finished.

From this extracted folder, on Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe top_n.py
.\.venv\Scripts\python.exe flatten_arrays.py
.\.venv\Scripts\python.exe malformed_csv.py
```

On macOS or Linux, create the environment with `python3 -m venv .venv` and substitute `.venv/bin/python` for the Windows interpreter path. Java must be available in the same environment; if JAVA_HOME is set it must identify the installed JDK. See the site's installation and Java gateway guides for setup help.

- `top_n.py`: exactly two rows per store and the alternative that includes cutoff ties.
- `flatten_arrays.py`: empty/null arrays, explode_outer, and unequal aligned arrays.
- `malformed_csv.py`: a numeric parsing error, a missing amount and a negative amount. Writes accepted and rejected Parquet directories, overwriting only this recipe's `output/csv_check` on each run. Keep original source files separately in a production pipeline. The sample uses DOUBLE for readable teaching examples; choose an appropriate DECIMAL schema for real monetary calculations.

The tiny in-memory datasets use SQL VALUES and array expressions, so these examples don't need a separate Python worker process. They still run real local Spark jobs. Only these small demonstration results are collected into Python for assertions.

Tutorials:
- https://profitabledonkeys.com/guides/pyspark-top-n-per-group
- https://profitabledonkeys.com/guides/pyspark-flatten-arrays
- https://profitabledonkeys.com/guides/pyspark-malformed-csv
