import re
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Iterator, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    BooleanType,
    ByteType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
    StructType,
    TimestampType,
)


class PyBujiaError(Exception):
    """Base exception for all PyBujia errors."""

    pass


class SchemaNotFoundError(PyBujiaError):
    """Exception raised when a fixture's table schema cannot be determined."""

    pass


class DataConversionError(PyBujiaError):
    """Raised when data conversion fails during table processing."""

    pass


class TableNotFoundError(PyBujiaError):
    """Raised when the requested table id does not exist."""

    pass


class DataParsingError(PyBujiaError):
    """Error parsing fixtures data."""

    pass


class PyBujia:
    def __init__(
        self,
        fixtures_file: str,
        spark: SparkSession,
        schemas_fetcher: Optional[Callable] = None,
    ) -> None:
        """Initializes a PyBujia object.

        Args:
            fixtures_file (str): Full path of the file with the data fixtures.
            spark (SparkSession): A Spark session, you can use helper.get_spark_session().
            schemas_fetcher (Optional[Callable]): Callback to fetch schema by table name.
        """

        self._spark = spark
        self._tables, self._schemas = self._load_fixtures_from_file(fixtures_file, schemas_fetcher)

    def get_table(self, name: str) -> list[dict[str, Any]]:
        """Gets the table data as a list of dictionaries.

        Args:
            name (str): Name of the table.

        Returns:
            list[dict[str, Any]]: Table data.

        Raises:
            TableNotFoundError: If table name does not exist.
            DataConversionError: If data conversion fails.
        """
        try:
            table = self._tables[name]
        except KeyError as ex:
            raise TableNotFoundError(f"Table not found '{name}'") from ex
        schema = self.get_schema(name)
        try:
            return self._convert_table(table, schema)
        except DataConversionError as ex:
            raise DataConversionError(f"Error converting table '{name}'") from ex

    def get_schema(self, name: str) -> StructType:
        """Gets the table's Spark schema.

        Args:
            name (str): Name of the table.

        Returns:
            StructType: The schema for the table.
        """
        return self._schemas[name]

    def get_dataframe(self, name: str) -> DataFrame:
        """Gets a Spark DataFrame from a table.

        Args:
            name (str): Name of the table.

        Returns:
            DataFrame: Spark DataFrame.
        """
        typed_table = self.get_table(name)
        schema = self.get_schema(name)
        return self._spark.createDataFrame(typed_table, schema)  # type: ignore

    @staticmethod
    def _clean_table_schema_id(table_schema_id: str) -> str:
        """Extracts a clean table schema ID from markdown link formatting.

        Args:
            table_schema_id (str): Raw table schema ID possibly formatted as markdown link.

        Returns:
            str: Clean table schema ID.
        """
        markdown_link_pattern = re.compile(
            r"""
            \[              # literal opening square bracket
            ([^\]]+)        # capture group: one or more characters that are NOT a closing square bracket
            \]              # literal closing square bracket
            \(              # literal opening parenthesis
            [^\)]+          # one or more characters that are NOT a closing parenthesis
            \)              # literal closing parenthesis
            """,
            re.VERBOSE,
        )

        clean_table_schema_id = table_schema_id.strip()
        potential_md_links = markdown_link_pattern.search(clean_table_schema_id)
        if potential_md_links:
            clean_table_schema_id = potential_md_links.group(1).strip()
        return clean_table_schema_id

    @classmethod
    def _extract_table_schema_id(cls, lines: list[str]) -> Optional[str]:
        """Extracts table schema ID from fixture lines if explicitly defined.

        Args:
            lines (list[str]): Lines from a fixture definition.

        Returns:
            Optional[str]: Extracted table schema ID if defined, else None.
        """
        table_schema_id = None
        for li in lines:
            if li.startswith("|"):
                break
            if re.match(r"^\s*Schema\s*:", li):
                raw_table_schema_id = li.split(":")[1]
                table_schema_id = cls._clean_table_schema_id(raw_table_schema_id)
                break
        return table_schema_id

    @staticmethod
    def _extract_data_lines(lines: list[str]) -> list[list[str]]:
        """Extracts rows of table data from fixture lines.

        Args:
            lines (list[str]): Lines from fixture definition.

        Returns:
            list[list[str]]: Extracted table rows, each row as list of column values.
        """
        pattern = re.compile(
            r"""
            \s*         # optional whitespace
            (?<!\\)     # not preceded by a backslash
            \|          # pipe character
            \s*         # optional whitespace
             """,
            re.VERBOSE,
        )

        return [
            [
                value.replace(r"\|", "|")  # Removing escape character \
                # Spliting by | considering escape char \ and ignoring first and last empty values
                for value in pattern.split(line.strip())[1:-1]
            ]
            for line in lines
            if line.startswith("|")
        ]

    @staticmethod
    def _is_markdown_table(data: list[list[str]]) -> bool:
        """Determines if table data is markdown-formatted.

        Args:
            data (list[list[str]]): Extracted data rows.

        Returns:
            bool: True if markdown format, False otherwise.
        """
        pattern = re.compile(
            r"""
            ^           # Start of line
            \s*         # Optional leading whitespace
            :?          # Optional colon (left align marker)
            -{3,}       # Thre or more dashes (the core of the divider)
            :?          # Optional colon (right align marker)
            \s*         # Optional trailing whitespace
            $           # End of line
            """,
            re.VERBOSE,
        )

        return all(pattern.match(value) for value in data[0])

    @classmethod
    def _extract_table(cls, lines: list[str]) -> tuple[list[dict], Optional[dict], Optional[str]]:
        """Extracts table data, schema definition, and table schema ID from fixture lines.

        Args:
            lines (list[str]): Lines from fixture table definition.

        Returns:
            tuple:
                - list[dict]: Table data as list of dictionaries.
                - Optional[dict]: Inline schema definition, if provided.
                - Optional[str]: table schema ID, if explicitly defined.
        """
        table_schema_id = cls._extract_table_schema_id(lines)
        data = cls._extract_data_lines(lines)
        header = data.pop(0)
        columns_names, data_types = cls._extract_col_names_and_types(header)
        if cls._is_markdown_table(data):
            data.pop(0)
        result_schema = None
        if not table_schema_id:
            # If no table schema id is defined and no data types were extracted from the header
            # the second line of data has the schema definition
            if not data_types:
                data_types = data.pop(0)

            # Removing backticks and stars from the data types values
            clean_data_types = map(lambda col_val: col_val.replace("`", "").replace("*", ""), data_types)
            result_schema = dict(zip(columns_names, clean_data_types))
        result_data = [dict(zip(columns_names, row)) for row in data]
        return result_data, result_schema, table_schema_id

    @staticmethod
    def _extract_col_names_and_types(header: list[str]) -> tuple[list[str], list[str]]:
        """Extracts column names and their types from table header.

        Args:
            header (list[str]): Header line of fixture table.

        Returns:
            tuple:
                - list[str]: Column names.
                - list[str]: Corresponding data types.

        Raises:
            DataParsingError: If columns are missing type definitions.
        """
        col_names = []
        data_types = []
        for val in header:
            val_split = val.split("[")
            name = val_split[0].strip()
            col_names.append(name)
            if len(val_split) > 1:
                col_type = val_split[1].replace("]", "").strip()
                data_types.append(col_type)
        if data_types and len(col_names) != len(data_types):
            raise DataParsingError(f"Some columns are missing the data types: {header}")
        return col_names, data_types

    @staticmethod
    def _read_fixture_file(path: str) -> str:
        """
        Read the contents of the fixture file.

        Args:
            path (str): Path to the fixture file.

        Returns:
            str: Contents of the file as a string.
        """
        with open(path) as f:
            return f.read()

    @staticmethod
    def _parse_fixture_blocks(content: str) -> Iterator[tuple[str, list[str]]]:
        """
        Parse raw fixture file content into named table blocks.

        Args:
            content (str): Full content of the fixture file.

        Yields:
            tuple[str, list[str]]: Each yielded item is a (table_name, lines) tuple.
        """

        pattern = re.compile(
            r"""
            ^           # Start of line
            \s*         # Optional leading whitespace
            \#*         # Zero or more '#' (Markdown heading levels)
            \s*         # Optional whitespace after heading
            Table:      # Literal label
            \s*         # Optional whitespace after colon
            """,
            re.VERBOSE | re.MULTILINE,
        )

        table_texts = pattern.split(content.strip())

        table_texts.pop(0)  # discard anything before the first Table:
        for table_section in table_texts:
            lines = table_section.split("\n")
            table_name = lines.pop(0).strip()
            yield table_name, lines

    @classmethod
    def _load_fixtures_from_file(
        cls, fixtures_file: str, schemas_fetcher: Optional[Callable] = None
    ) -> tuple[dict[str, list[dict]], dict[str, StructType]]:
        """Loads fixture data from file, extracting tables and their schemas.

        Args:
            fixtures_file (str): Path to fixtures file.
            schemas_fetcher (Optional[Callable]): Callback to fetch schema by table schema ID.

        Returns:
            tuple:
                - dict[str, list[dict]]: Extracted tables and their data.
                - dict[str, StructType]: Extracted tables and their schemas.

        Raises:
            SchemaNotFoundError: If table schema ID is found but no schemas_fetcher was provided.
        """
        file_content = cls._read_fixture_file(fixtures_file)
        table_blocks = cls._parse_fixture_blocks(file_content)

        tables = {}
        schemas = {}

        for table_name, lines in table_blocks:
            extracted_table, extracted_schema, table_schema_id = cls._extract_table(lines)

            if table_schema_id and not schemas_fetcher:
                raise SchemaNotFoundError(
                    f"Table id '{table_name}' has the table schema id: "
                    f"'{table_schema_id}' but no schema fetcher was provided"
                )

            tables[table_name] = extracted_table

            if table_schema_id and schemas_fetcher:
                schemas[table_name] = schemas_fetcher(table_schema_id)
            elif extracted_schema is not None:
                schemas[table_name] = cls._convert_to_struct_type(extracted_schema)

        return tables, schemas

    @staticmethod
    def _convert_to_struct_type(dict_schema: dict[str, str]) -> StructType:
        """Converts dictionary-based schema definitions into Spark StructType.

        Args:
            dict_schema (dict[str, str]): Column definitions with data types.

        Returns:
            StructType: Corresponding Spark schema.
        """
        fields = []
        for col_name, col_type in dict_schema.items():
            col_type = col_type.lower().strip()
            clean_col_type, num_replacements = re.subn(r"\s+not\s+null\s*", "", col_type)
            nullable = num_replacements == 0
            fields.append({"name": col_name, "type": clean_col_type, "metadata": {}, "nullable": nullable})
        return StructType.fromJson({"fields": fields, "type": "struct"})

    @staticmethod
    def _get_typed_val(col_type: Optional[DataType], col_value: Any) -> Any:
        """Converts a raw column value accordingly to its corresponding PySpark typed value.

        Args:
            col_type (Optional[DataType]): Spark data type.
            col_value (Any): Raw column value.

        Returns:
            Any: Converted typed value.

        Raises:
            DataConversionError: If conversion fails due to incorrect format.
        """
        if col_value == "<NULL>":
            return None
        if isinstance(col_type, DecimalType):
            return Decimal(col_value)
        if isinstance(col_type, (FloatType, DoubleType)):
            return float(col_value)
        if isinstance(col_type, (ShortType, ByteType, IntegerType, LongType)):
            return int(col_value)
        if isinstance(col_type, DateType):
            return datetime.strptime(col_value, "%Y-%m-%d")
        if isinstance(col_type, TimestampType):
            try:
                return datetime.strptime(col_value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(col_value, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(col_type, BooleanType):
            if col_value == "false":
                return False
            elif col_value == "true":
                return True
            else:
                return None
        return col_value

    @classmethod
    def _convert_table(cls, table: list[dict], schema: StructType) -> list[dict]:
        """Converts raw table data to typed representations according to schema.

        Args:
            table (list[dict]): Raw table data from fixtures.
            schema (StructType): Spark schema defining data types.

        Returns:
            list[dict]: Typed table data.

        Raises:
            DataConversionError: If conversion fails for any column.
        """
        result = []
        data_types = {field.name: field.dataType for field in schema}
        for row in table:
            typed_row = {}
            for col_name, col_value in row.items():
                try:
                    col_type = data_types[col_name]
                except KeyError as ex:
                    raise DataConversionError(f"Column '{col_name}' not found in the schema") from ex
                try:
                    typed_val = cls._get_typed_val(col_type, col_value)
                except Exception as ex:
                    raise DataConversionError(
                        f"Error converting field: '{col_name}', '{col_value}', '{col_type}'"
                    ) from ex
                typed_row[col_name] = typed_val
            result.append(typed_row)
        return result
