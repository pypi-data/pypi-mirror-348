# 🔍 PySpark Data Quality Framework

A flexible, extensible PySpark-based Data Quality (DQ) framework designed to apply configurable data quality checks on Spark DataFrames using a YAML-based rule system.

---

## 📦 Installation

- Install the package from PyPI:

```bash
pip install pyspark-dq-framework

Ensure pyspark is installed:
```
pip install pyspark
```

📁 Project Structure
pyspark_dq_framework/
├── config.yml                 # YAML configuration file for data quality rules
├── dq_functions.py           # Core data quality functions
├── dq_config.py              # YAML parser to config DataFrame
├── run_dq_check.py           # Engine to run checks with logging
├── main.py                   # Example usage script
└── README.md                 # Documentation

📘 Module Descriptions
1. config.yml – Define DQ Rules
Stores DQ rules for tables and columns

YAML format, human-readable and configurable

Sample:
model:
  - name: df
    columns:
      - name: ID
        checks:
          - null_check
          - unique_check
      - name: Age
        checks:
          - null_check

2. dq_functions.py – Built-in DQ Checks
Contains all reusable data quality functions

Supported Checks:

null_check

unique_check

set_membership_check

range_check

non_negative_check

regex_check

not_empty_check

data_type_check

Each check returns:

valid_df: rows that passed

invalid_df: rows that failed

log_df: log entry of the check

from dq_functions import null_check

valid_df, invalid_df, log_df = null_check(df, {"table": "df", "column": "ID"})

3. dq_config.py – Parse YAML Config
Reads config.yml and flattens it into a Spark DataFrame

Function:
from dq_config import dq_config

dq_config_df = dq_config(spark)

Returns a DataFrame like:
+-------+--------+-------------+
| table | column | check       |
+-------+--------+-------------+
| df    | ID     | null_check  |
| df    | ID     | unique_check|
| df    | Age    | null_check  |
+-------+--------+-------------+

4. run_dq_check.py – Run and Log DQ Checks
Executes each check defined in config

Logs check result and error records

Function:
from run_dq_check import run_dq_checks_with_error_handling

clean_df, all_errors_df, enriched_logs_df = run_dq_checks_with_error_handling(
    df, dq_config_df, check_function_map
)

Returns:

clean_df: all valid rows

all_errors_df: union of invalid rows from all checks

enriched_logs_df: metadata logs + JSON error list

🚀 How to Use (main.py)
Steps:
Start Spark Session

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DQExample").getOrCreate()

Create Sample DataFrame
data = [(1, "Alice", 34), (None, "Bob", 45)]
df = spark.createDataFrame(data, ["ID", "Name", "Age"])

Create YAML Config (config.yml)
model:
  - name: df
    columns:
      - name: ID
        checks:
          - null_check
      - name: Age
        checks:
          - null_check

Load Config
from dq_config import dq_config
dq_config_df = dq_config(spark)

Map Check Functions

from dq_functions import *

check_function_map = {
    "null_check": null_check,
    "unique_check": unique_check,
    "set_membership_check": lambda df, row: set_membership_check(df, row, allowed_values=["Alice", "Bob"]),
    "range_check": lambda df, row: range_check(df, row, min_value=0, max_value=100),
    "non_negative_check": non_negative_check,
    "regex_check": lambda df, row: regex_check(df, row, pattern=r"^[a-zA-Z]+$"),
    "not_empty_check": not_empty_check,
    "data_type_check": data_type_check
}

Run DQ Checks
from run_dq_check import run_dq_checks_with_error_handling

clean_df, error_df, logs_df = run_dq_checks_with_error_handling(
    df, dq_config_df, check_function_map
)

Inspect Results
clean_df.show()
error_df.show()
logs_df.show(truncate=False)


🧪 Supported Environments
Python 3.7+

Apache Spark 3.x+

Local or Cluster Spark Deployments

📖 Example Output
Logs Output:

+-----+--------+-------------+-------+--------------+-------------------------+
|table|column  |check_type   |passed|invalid_count |error_data_json          |
+-----+--------+-------------+------+--------------+-------------------------+
|df   |ID      |null_check   |false |1             |["{\"Name\":\"Bob\",..."]
+-----+--------+-------------+------+--------------+-------------------------+


🔧 Extending the Framework
To add a custom check:

Define a new function in dq_functions.py

Make sure it returns: valid_df, invalid_df, log_df

Add it to your check_function_map in main.py

🧑‍💻 Contributing
Fork the repository

Add your improvements or new checks

Submit a pull request 🚀

📄 License
This project is licensed under the MIT License.

💬 Questions or Feedback?
Open an issue

Start a discussion in the GitHub repository
