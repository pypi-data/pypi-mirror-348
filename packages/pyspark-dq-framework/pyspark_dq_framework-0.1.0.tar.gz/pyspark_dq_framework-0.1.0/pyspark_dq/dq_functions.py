from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, row_number
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

# Common schema for error logs
error_schema = StructType([
    StructField("table", StringType()),
    StructField("column", StringType()),
    StructField("check_type", StringType()),
    StructField("passed", BooleanType()),
    StructField("invalid_count", IntegerType())
])


def create_log_df(df, table, column, check_type, passed, count):
    return df.sparkSession.createDataFrame(
        [(table, column, check_type, passed, count)],
        schema=error_schema
    )


def null_check(df, row):
    table = row["table"]
    column = row["column"]
    check_type = "null_check"

    valid_df = df.filter(col(column).isNotNull())
    invalid_df = df.filter(col(column).isNull()) \
                   .withColumn("table", lit(table)) \
                   .withColumn("column", lit(column)) \
                   .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def unique_check(df, row):
    table = row["table"]
    column = row["column"]
    check_type = "unique_check"

    window_spec = Window.partitionBy(column).orderBy(column)
    df_with_rn = df.withColumn("row_num", row_number().over(window_spec))

    valid_df = df_with_rn.filter(col("row_num") == 1).drop("row_num")
    invalid_df = df_with_rn.filter(col("row_num") > 1).drop("row_num") \
                           .withColumn("table", lit(table)) \
                           .withColumn("column", lit(column)) \
                           .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def set_membership_check(df, row, allowed_values):
    table = row["table"]
    column = row["column"]
    check_type = "set_membership_check"

    valid_df = df.filter(col(column).isin(allowed_values))
    invalid_df = df.filter(~col(column).isin(allowed_values)) \
                   .withColumn("table", lit(table)) \
                   .withColumn("column", lit(column)) \
                   .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def range_check(df, row, min_value=None, max_value=None):
    table = row["table"]
    column = row["column"]
    check_type = "range_check"

    condition = None
    if min_value is not None and max_value is not None:
        condition = (col(column) >= min_value) & (col(column) <= max_value)
    elif min_value is not None:
        condition = col(column) >= min_value
    elif max_value is not None:
        condition = col(column) <= max_value

    valid_df = df.filter(condition)
    invalid_df = df.filter(~condition) \
                   .withColumn("table", lit(table)) \
                   .withColumn("column", lit(column)) \
                   .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def non_negative_check(df, row):
    table = row["table"]
    column = row["column"]
    check_type = "non_negative_check"

    valid_df = df.filter(col(column) >= 0)
    invalid_df = df.filter(col(column) < 0) \
                   .withColumn("table", lit(table)) \
                   .withColumn("column", lit(column)) \
                   .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def regex_check(df, row, pattern):
    table = row["table"]
    column = row["column"]
    check_type = "regex_check"

    valid_df = df.filter(col(column).rlike(pattern))
    invalid_df = df.filter(~col(column).rlike(pattern)) \
                   .withColumn("table", lit(table)) \
                   .withColumn("column", lit(column)) \
                   .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, invalid_df.count() == 0, invalid_df.count())
    return valid_df, invalid_df, log_df


def not_empty_check(df, row):
    table = row["table"]
    column = row["column"]  # for schema compatibility
    check_type = "not_empty_check"

    passed = df.count() > 0

    valid_df = df if passed else df.limit(0)
    invalid_df = df.limit(0) if passed else df \
        .withColumn("table", lit(table)) \
        .withColumn("column", lit(column)) \
        .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, passed, 0 if passed else df.count())
    return valid_df, invalid_df, log_df


def data_type_check(df, row):
    table = row["table"]
    column = row["column"]
    check_type = "data_type_check"
    expected_type = row.get("expected_type")  # Must be provided in config

    actual_type = next((f.dataType.simpleString() for f in df.schema.fields if f.name == column), None)
    passed = actual_type == expected_type

    valid_df = df if passed else df.limit(0)
    invalid_df = df.limit(0) if passed else df \
        .withColumn("table", lit(table)) \
        .withColumn("column", lit(column)) \
        .withColumn("check_type", lit(check_type))

    log_df = create_log_df(df, table, column, check_type, passed, 0 if passed else df.count())
    return valid_df, invalid_df, log_df