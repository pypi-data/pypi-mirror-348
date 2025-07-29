from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, struct, to_json, collect_list
from typing import Tuple

def run_dq_checks_with_error_handling(
    df: DataFrame,
    dq_config_df: DataFrame,
    check_function_map: dict
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    """
    Run DQ checks on a DataFrame using config and return:
    - clean_df: DataFrame with valid records across all checks.
    - all_errors_df: Union of all failed records from all checks.
    - all_logs_df: One row per check, includes error JSON array in 'error_data_json'.

    Returns:
    -------
    Tuple[DataFrame, DataFrame, DataFrame]
    """

    spark = df.sparkSession
    clean_df = df
    all_errors_df = None
    all_logs_df = None

    config_rows = dq_config_df.collect()

    for row in config_rows:
        check_name = row["check"]
        check_func = check_function_map.get(check_name)

        if check_func:
            try:
                valid_df, invalid_df, log_df = check_func(clean_df, row)

                clean_df = valid_df

                # Accumulate errors
                if all_errors_df:
                    all_errors_df = all_errors_df.unionByName(invalid_df)
                else:
                    all_errors_df = invalid_df

                # Accumulate logs
                if all_logs_df:
                    all_logs_df = all_logs_df.unionByName(log_df)
                else:
                    all_logs_df = log_df

            except Exception as e:
                print(f"Error running {check_name} on column {row['column']}: {str(e)}")

                error_schema = spark.createDataFrame([], """
                    table STRING, column STRING, check_type STRING, passed BOOLEAN, invalid_count INT
                """).schema

                error_row = spark.createDataFrame(
                    [(row['table'], row['column'], check_name, False, 0)],
                    schema=error_schema
                )

                if all_logs_df:
                    all_logs_df = all_logs_df.unionByName(error_row)
                else:
                    all_logs_df = error_row
        else:
            print(f"No check function found for '{check_name}'")

    # If no errors occurred
    if all_errors_df is None:
        all_errors_df = df.limit(0)

    if all_logs_df is None:
        all_logs_df = spark.createDataFrame([], """
            table STRING, column STRING, check_type STRING, passed BOOLEAN, invalid_count INT
        """)

    # Prepare error_data_json by grouping per check
    error_json_df = (
        all_errors_df
        .withColumn("error_json", to_json(struct(*[c for c in all_errors_df.columns if c not in ['table', 'column', 'check_type']])))
        .groupBy("table", "column", "check_type")
        .agg(collect_list("error_json").alias("error_data_json"))
    )

    # Join logs with JSON error data
    enriched_logs_df = all_logs_df.join(error_json_df, on=["table", "column", "check_type"], how="left")

    return clean_df, all_errors_df, enriched_logs_df