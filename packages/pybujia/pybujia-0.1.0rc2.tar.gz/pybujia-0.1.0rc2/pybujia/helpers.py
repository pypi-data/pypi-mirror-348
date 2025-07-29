import json
import math
import os
import inspect
from typing import Any, Callable, Optional
from decimal import Decimal

from . import PyBujia

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType


def compare_dicts(result_row: dict[str, Any], expected_row: dict[str, Any], float_abs_tol: float = 1e-9) -> None:
    """Compares two dictionaries field-by-field using absolute tolerance for floats.

    Args:
        result_row (dict): Actual result dictionary.
        expected_row (dict): Expected result dictionary.
        float_abs_tol (float): Absolute tolerance for float/decimal comparison.

    Raises:
        ValueError: If a key is missing in the expected row.
        AssertionError: If any value mismatches.
    """
    for field, result_value in result_row.items():
        try:
            expected_value = expected_row[field]
        except KeyError as ex:
            raise ValueError(f"The column '{field}' doesn't exist in the expected result row {expected_row}") from ex

        if isinstance(result_value, (float, Decimal)) and isinstance(expected_value, (float, Decimal)):
            assert math.isclose(result_value, expected_value, rel_tol=0.0, abs_tol=float_abs_tol), (
                f"Field '{field}' mismatch: {result_value} != {expected_value} "
                f"(float_abs_tol={float_abs_tol}) — Row: {result_row} vs {expected_row}"
            )
        else:
            assert result_value == expected_value, (
                f"Field '{field}' mismatch: {result_value!r} != {expected_value!r} "
                f"({type(result_value)} vs {type(expected_value)}) — Row: {result_row} vs {expected_row}"
            )


def compare_dfs(result_df: DataFrame, expected_df: DataFrame, float_abs_tol: float = 1e-9) -> None:
    """Compares two Spark DataFrames for content equality.

    Args:
        result_df (DataFrame): Actual DataFrame.
        expected_df (DataFrame): Expected DataFrame.
        float_abs_tol (float): Absolute tolerance for float/decimal comparison.

    Raises:
        AssertionError: If row counts or contents differ.
    """
    result = result_df.orderBy(*result_df.columns).collect()
    expected = expected_df.orderBy(*expected_df.columns).collect()

    result_len = len(result)
    expected_len = len(expected)
    assert (
        result_len == expected_len
    ), f"Rows count mismatch:, len(result_df)={result_len=} != len(expected_df){expected_len=}"

    for result_row, expected_row in zip(result, expected):
        compare_dicts(
            result_row.asDict(),
            expected_row.asDict(),
            float_abs_tol,
        )


def compare_dfs_schemas(
    result_schema: StructType,
    expected_schema: StructType,
    check_nullability: bool = False,
) -> None:
    """Compares two Spark schemas for equality.

    Args:
        result_schema (StructType): Actual schema.
        expected_schema (StructType): Expected schema.
        check_nullability (bool): Whether to include nullability in comparison.

    Raises:
        AssertionError: If schemas differ.
    """
    result_columns = [
        (f.name, f.dataType.simpleString(), f.nullable if check_nullability else None) for f in result_schema.fields
    ]
    expected_columns = [
        (f.name, f.dataType.simpleString(), f.nullable if check_nullability else None) for f in expected_schema.fields
    ]
    assert result_columns == expected_columns, f"Schemas mismatch found: {result_schema} != {expected_schema}"


def get_spark_session(
    warehouse_dir: Optional[str] = None,
    extra_configs: Optional[dict[str, str]] = None,
) -> SparkSession:
    """Creates a local SparkSession configured for testing.

    Args:
        warehouse_dir (Optional[str]): Optional warehouse directory.
        extra_configs (Optional[dict[str, str]]): Additional Spark configs.

    Returns:
        SparkSession: Configured Spark session.
    """
    if warehouse_dir is None:
        caller_file = inspect.stack()[1].filename
        warehouse_dir = os.path.join(os.path.dirname(caller_file), "pyspark-data")

    builder = (
        SparkSession.builder.appName("unit-tests")
        .config("spark.driver.extraJavaOptions", "-Duser.timezone=GMT")
        .config("spark.executor.extraJavaOptions", "-Duser.timezone=GMT")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", 1)
        .config("spark.sql.warehouse.dir", warehouse_dir)
    )

    if extra_configs is not None:
        for key, value in extra_configs.items():
            builder = builder.config(key, value)

    return builder.master("local[1]").getOrCreate()


def get_table_schema(db_name: str, table_name: str, base_path: str) -> StructType:
    """Loads a schema JSON file and converts it to StructType.

    Args:
        db_name (str): Database name.
        table_name (str): Table name.
        base_path (str): Root path to schemas.

    Returns:
        StructType: Parsed schema.
    """
    schema_path = os.path.join(base_path, db_name, f"{table_name}.json")
    with open(schema_path) as f:
        schema = json.load(f)

    for field in schema["fields"]:
        field["metadata"] = field.get("metadata", {})
        field["nullable"] = field.get("nullable", True)

    return StructType.fromJson(schema)


def spark_job_test(
    spark_session: SparkSession,
    input_tables: list[tuple],
    output_tables: list[tuple],
    run_spark_job: Callable,
    fixtures: PyBujia,
    no_assert: bool = False,
    expected_table_suffix: str = "__expected",
) -> None:
    """Runs a Spark job with data populated from fixtures and validates output.

    Args:
        spark_session (SparkSession): Active Spark session.
        input_tables (list[tuple]): List of (db, table) for input.
        output_tables (list[tuple]): List of (db, table) for output.
        run_spark_job (Callable): Function that runs the Spark job.
        fixtures (PyBujia): Fixture loader instance.
        no_assert (bool): Whether to skip result assertions.
        expected_table_suffix (str): suffix for the expected tables names.

    Raises:
        AssertionError: If actual output does not match expected output.
    """
    tables_to_create = [(db, table) for db, table in input_tables]
    tables_to_create.extend((db, table + expected_table_suffix) for db, table in output_tables)

    dbs_used = {db for db, _ in tables_to_create}
    for db_name in dbs_used:
        spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    for db_name, table_name in tables_to_create:
        full_table_name = f"{db_name}.{table_name}"
        test_df = fixtures.get_dataframe(full_table_name)
        test_df.write.mode("overwrite").saveAsTable(full_table_name)

    run_spark_job()

    if no_assert:
        return

    for db_name, table_name in output_tables:
        full_table_name = f"{db_name}.{table_name}"
        result_df = spark_session.table(full_table_name)
        expected_result_table_name = full_table_name + expected_table_suffix
        expected_result_df = spark_session.table(expected_result_table_name)
        compare_dfs(result_df, expected_result_df)
