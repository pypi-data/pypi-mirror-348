import os
import shutil
from datetime import datetime

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    IntegerType,
    DateType,
    DoubleType,
    StringType,
    StructField,
    StructType,
)

from pybujia import (
    PyBujia,
    SchemaNotFoundError,
)

from pybujia.helpers import (
    compare_dfs,
    compare_dfs_schemas,
    get_spark_session,
    get_table_schema,
)


class TestPyBujia:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_FIXTURES_PATH = os.path.join(CURRENT_DIR, "pybujia.tests.md")
    PYSPARK_DATA_DIR = os.path.join(CURRENT_DIR, "pyspark-data")

    _spark: SparkSession

    @classmethod
    def setup_class(cls) -> None:
        cls.teardown_class()

        cls._spark = get_spark_session(cls.PYSPARK_DATA_DIR)

    @classmethod
    def teardown_class(cls) -> None:
        shutil.rmtree(cls.PYSPARK_DATA_DIR, ignore_errors=True)

    @classmethod
    def schemas_fetcher(cls, table_name: str) -> StructType:
        db_name, table_name, *_ = table_name.split(".")
        return get_table_schema(db_name, table_name, base_path=os.path.join(cls.CURRENT_DIR, "schemas"))

    def test__test_fixtures_class(self) -> None:
        fixtures = PyBujia(self.FILE_FIXTURES_PATH, self._spark, self.schemas_fetcher)
        expected_tables = {
            "table_1": [
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 11, 1, 0, 0),
                    "some_value": 2.0,
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 9, 1, 0, 0),
                    "some_value": 0.0,
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 8, 1, 0, 0),
                    "some_value": 4.0,
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 7, 1, 0, 0),
                    "some_value": 5.0,
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 5, 1, 0, 0),
                    "some_value": 7.55,
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 4, 1, 0, 0),
                    "some_value": 41.2,
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 3, 1, 0, 0),
                    "some_value": 1100.68,
                },
            ],
            "table_2": [
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 11, 1, 0, 0),
                    "some_value": 4.0,
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 9, 1, 0, 0),
                    "some_value": 20.0,
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 8, 1, 0, 0),
                    "some_value": 6.0,
                },
                {
                    "col1": "cat1|0",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 7, 1, 0, 0),
                    "some_value": 7.0,
                },
                {
                    "col1": "cat2|0",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 5, 1, 0, 0),
                    "some_value": 27.55,
                },
                {
                    "col1": "cat2|0",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 4, 1, 0, 0),
                    "some_value": 61.2,
                },
                {
                    "col1": "cat2|0",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 3, 1, 0, 0),
                    "some_value": 2200.68,
                },
            ],
        }

        assert expected_tables["table_1"] == fixtures.get_table("table_1")

        assert expected_tables["table_1"] == fixtures.get_table("table_md_format")

        assert expected_tables["table_2"] == fixtures.get_table("table_2")

        result_df = fixtures.get_dataframe("table_2")

        expected_schema = StructType(
            [
                StructField("col1", StringType(), True),
                StructField("col2", StringType(), True),
                StructField("col3", StringType(), True),
                StructField("col4", StringType(), True),
                StructField("some_date", DateType(), True),
                StructField("some_value", DoubleType(), True),
            ]
        )
        compare_dfs_schemas(result_df.schema, expected_schema, check_nullability=True)

    @pytest.mark.parametrize(
        "input_str, cleaned_id",
        [
            ("   alpha_db.alpha_table   ", "alpha_db.alpha_table"),
            ("[beta_db.beta_table](../schemas/beta_db/beta_table.json)", "beta_db.beta_table"),
            ("[  gamma_db.gamma_table  ](../schemas/other_schema/schema.json)", "gamma_db.gamma_table"),
        ],
    )
    def test_table_schema_id_stripped_and_extracted_properly(self, input_str, cleaned_id):
        normalized = PyBujia._clean_table_schema_id(input_str)
        assert normalized == cleaned_id

    def test__test_fixtures_class_no_schema(self) -> None:
        with pytest.raises(SchemaNotFoundError) as ex:
            PyBujia(self.FILE_FIXTURES_PATH, self._spark)
        assert str(ex.value) == (
            "Table id 'table_schema_fetcher_1' has the table schema id: "
            "'my_fixtures_db.my_fixtures_table' but no schema fetcher was provided"
        )

    def test__test_fixtures_class_schema_fetcher(self) -> None:
        fixtures = PyBujia(self.FILE_FIXTURES_PATH, self._spark, self.schemas_fetcher)
        result_df1 = fixtures.get_dataframe("table_schema_fetcher_1")
        result_df2 = fixtures.get_dataframe("table_schema_fetcher_2")

        expected_output = [
            {"my_col1": "alpha", "my_col2": 9},
            {"my_col1": "beta", "my_col2": 8},
            {"my_col1": "gamma", "my_col2": 7},
        ]
        expected_schema = StructType(
            [
                StructField("my_col1", StringType(), True),
                StructField("my_col2", IntegerType(), True),
            ]
        )
        expected_df = self._spark.createDataFrame(expected_output, expected_schema)  # type: ignore
        compare_dfs(result_df1, expected_df)
        compare_dfs(result_df2, expected_df)

        compare_dfs_schemas(result_df1.schema, expected_df.schema)
        compare_dfs_schemas(result_df2.schema, expected_df.schema)

    def test_compare_dfs_schemas_matching_without_nullability(self) -> None:
        schema1 = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), False),
            ]
        )
        schema2 = StructType(
            [
                StructField("name", StringType(), False),  # nullability ignored
                StructField("age", IntegerType(), True),
            ]
        )
        compare_dfs_schemas(schema1, schema2, check_nullability=False)

        def test_compare_dfs_schemas_matching_with_nullability(self) -> None:
            schema1 = StructType(
                [
                    StructField("name", StringType(), True),
                    StructField("age", IntegerType(), False),
                ]
            )
            schema2 = StructType(
                [
                    StructField("name", StringType(), True),
                    StructField("age", IntegerType(), False),
                ]
            )
            compare_dfs_schemas(schema1, schema2, check_nullability=True)

        def test_compare_dfs_schemas_mismatched_column_name(self) -> None:
            schema1 = StructType(
                [
                    StructField("name", StringType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("full_name", StringType(), True),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2)

        def test_compare_dfs_schemas_mismatched_data_type(self) -> None:
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", StringType(), True),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2)

        def test_compare_dfs_schemas_mismatched_nullability_with_check(self) -> None:
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", IntegerType(), False),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2, check_nullability=True)

        def test_compare_dfs_schemas_ignore_nullability_difference(self) -> None:
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", IntegerType(), False),
                ]
            )
            compare_dfs_schemas(schema1, schema2, check_nullability=False)

    def test_compare_dfs_schemas_column_order_matters(self) -> None:
        schema1 = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True),
            ]
        )
        schema2 = StructType(
            [
                StructField("age", IntegerType(), True),
                StructField("name", StringType(), True),
            ]
        )
        with pytest.raises(AssertionError):
            compare_dfs_schemas(schema1, schema2)
