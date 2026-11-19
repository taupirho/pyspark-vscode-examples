"""Print local setup details without starting Spark or changing configuration."""
import importlib.util
import os
import shutil
import subprocess
import sys

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version.split()[0]}")
spec = importlib.util.find_spec("pyspark")
print(f"PySpark module: {spec.origin if spec else 'NOT INSTALLED in this interpreter'}")
print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', '(unset)')}")
java = shutil.which("java")
print(f"Java on PATH: {java or 'NOT FOUND'}")
if java:
    subprocess.run([java, "-version"], check=False)

