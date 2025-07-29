import yaml
from pyspark.sql.types import StructType, StructField, StringType

def dq_config(spark):
    """
    Load a YAML-based data quality (DQ) configuration file (config.yml),
    flatten its structure into a list of DQ rule entries, and return it 
    as a PySpark DataFrame for downstream processing.

    Parameters:
    ----------
    spark : pyspark.sql.SparkSession
        The active Spark session used to create the DataFrame.

    Returns:
    -------
    dq_config_df : pyspark.sql.DataFrame
        A DataFrame containing three columns: 'table', 'name', and 'checks',
        where each row represents a single DQ check for a given table and column.

    Example Schema:
    ---------------
    +------------+----------+-------------+
    | table      | name     | checks      |
    +------------+----------+-------------+
    | customers  | email    | null_check  |
    | orders     | order_id | unique_check|
    +------------+----------+-------------+

    Notes:
    ------
    - The function expects the YAML file to follow this structure:
        model:
          - name: table_name
            columns:
              - name: column_name
                checks:
                  - null_check
                  - unique_check
    - If the YAML contains nested dicts in checks (e.g. range_check: {min: 0}), 
      these should be converted to strings or handled separately.

    Assumptions:
    ------------
    - The YAML file is named 'config.yml' and is located in the current working directory.
    - The 'checks' are always list items (strings or simple dicts), not complex objects.

    """

    # Load the YAML file
    with open("config.yml", "r") as f:
        yml_data = yaml.safe_load(f)

    # Flatten YAML into list of dicts
    records = []

    for model in yml_data.get("model", []):
        table_name = model.get("name")
        for col in model.get("columns", []):
            col_name = col.get("name")
            for check in col.get("checks", []):
                records.append({
                    "table": table_name,
                    "column": col_name,
                    "check": check
                })
    
    # Defining Schema
    schema = StructType([
        StructField("table", StringType(), True),
        StructField("column", StringType(), True),
        StructField("check", StringType(), True)
    ])

    # Convert to PySpark DataFrame
    dq_config_df = spark.createDataFrame(records,schema)

    return dq_config_df