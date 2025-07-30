import os
import shutil

from typing import Final

from pybujia import PyBujia

from pybujia.helpers import (
    get_spark_session,
    spark_job_test,
)

from pyspark.sql import SparkSession

from user_retention.user_actions_job import UserActionsJob


class TestUserActionsJob:
    CURRENT_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
    PYSPARK_DATA_DIR: Final[str] = os.path.join(CURRENT_DIR, "pyspark-data")

    _spark: SparkSession

    @classmethod
    def setup_class(cls) -> None:
        cls.teardown_class()

        cls._spark = get_spark_session(cls.PYSPARK_DATA_DIR)

        all_tables = UserActionsJob.INPUT_TABLES + UserActionsJob.OUTPUT_TABLES
        all_dbs = {db for db, _ in all_tables}
        for db in all_dbs:
            cls._spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")

    @classmethod
    def teardown_class(cls) -> None:
        shutil.rmtree(cls.PYSPARK_DATA_DIR, ignore_errors=True)

    def test_user_actions_job_example(self) -> None:
        fixtures = PyBujia(
            os.path.join(self.CURRENT_DIR, "example.tests.md"),
            self._spark,
        )
        spark_job_test(
            self._spark,
            UserActionsJob.INPUT_TABLES,
            UserActionsJob.OUTPUT_TABLES,
            lambda: UserActionsJob(self._spark).run(),
            fixtures,
        )

    def test_user_actions_job_solution(self) -> None:
        fixtures = PyBujia(
            os.path.join(self.CURRENT_DIR, "solution.tests.md"),
            self._spark,
        )
        spark_job_test(
            self._spark,
            UserActionsJob.INPUT_TABLES,
            UserActionsJob.OUTPUT_TABLES,
            lambda: UserActionsJob(self._spark).run(),
            fixtures,
        )
