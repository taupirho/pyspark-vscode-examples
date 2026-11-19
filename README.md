# Run and debug PySpark in VS Code

A free companion to the [Profitable Donkeys installation guide](https://profitabledonkeys.com/guides/pyspark-local-installation?utm_source=github&utm_medium=referral&utm_campaign=pyspark_setup_nov26).

Use Python 3.13 and Java 21 for the version combination used by these examples. PySpark is pinned to 4.2.0 for reproducibility.

Open this folder itself in VS Code. Install Microsoft's Python and Python Debugger extensions.

## Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe diagnose.py
.\.venv\Scripts\python.exe setup_check.py
```

## WSL, Ubuntu or macOS

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python diagnose.py
.venv/bin/python setup_check.py
```

Install Java inside WSL if that is where you run Python. If local Windows Hadoop file permissions prevent the write, use WSL with the project under your Linux home directory.

The successful run prints Spark version 4.2.0, Master URL local[2], and Rows written 2. Spark also writes diagnostic logs. Each run overwrites only this example's output/setup_check directory. This example uses spark.range so it can verify Java and file output without requiring a separate Python worker.

## Debug

Run **Python: Select Interpreter** and choose this folder's `.venv`. Open a new terminal. Put a breakpoint on `rows_written = result.count()`, select **Debug local PySpark setup**, then press F5. Step over with F10 and inspect `rows_written` in Variables. This debugs the Python driver. Python UDF workers and the JVM execute separately.

Read the [VS Code debugging walkthrough](https://profitabledonkeys.com/guides/debug-pyspark-vscode?utm_source=github&utm_medium=referral&utm_campaign=pyspark_setup_nov26), the [Java gateway troubleshooting guide](https://profitabledonkeys.com/guides/pyspark-java-gateway-error), or the [missing PySpark module guide](https://profitabledonkeys.com/guides/no-module-named-pyspark-vscode).
