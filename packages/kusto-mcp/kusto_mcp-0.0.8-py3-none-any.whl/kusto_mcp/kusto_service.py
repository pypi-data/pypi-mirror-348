import inspect
import os
import uuid
from itertools import islice
from typing import Any, Dict, List, Optional, cast

from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import IngestionProperties, IngestionResult
from mcp.server.fastmcp import FastMCP

from kusto_mcp.kusto_config import KustoConfig
from kusto_mcp.kusto_connection import KustoConnection
from kusto_mcp.kusto_response_formatter import format_results

from . import __version__

# MCP server
mcp = FastMCP("kusto-mcp-server")


class KustoService:
    _conn: Optional[KustoConnection] = None
    DESTRUCTIVE_TOOLS = {
        "execute_command",
        "ingest_inline_into_table",
        "ingest_csv_file_to_table",
    }

    def __init__(self, config: KustoConfig):
        self.config = config

    @property
    def conn(self) -> KustoConnection:
        if self._conn is None:
            self._conn = KustoConnection(self.config)
        return self._conn

    def execute_query(
        self, query: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(query, database=database)

    def execute_command(
        self, command: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(command, database=database)

    def print_file(self, file_abs_path: str, lines_number: int = -1) -> str:
        try:
            if lines_number == -1:
                with open(file_abs_path, "r") as f:
                    return f.read()

            with open(file_abs_path) as input_file:
                return "".join(islice(input_file, lines_number))
        except FileNotFoundError:
            return f"Error: File not found: {file_abs_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def ingest_csv_file_to_table(
        self,
        destination_table_name: str,
        file_abs_path: str,
        ignore_first_record: bool,
        database: Optional[str] = None,
    ) -> IngestionResult:
        database = database or self.config.database_name
        if not database:
            raise ValueError(
                "Database name must be provided either in the config or as an argument."
            )
        ingest_client = self.conn.ingestion_client
        ingestion_properties = IngestionProperties(
            database=database,
            table=destination_table_name,
            data_format=DataFormat.CSV,
            ignore_first_record=ignore_first_record,
        )

        # ingest from file
        file_abs_path = os.path.normpath(file_abs_path)
        self._run_clear_streamingingestion_schema()
        return ingest_client.ingest_from_file(
            file_abs_path, ingestion_properties=ingestion_properties
        )

    def list_databases(self) -> List[Dict[str, Any]]:
        return self._execute(".show databases")

    def list_tables(self, database: str) -> List[Dict[str, Any]]:
        return self._execute(".show tables", database=database)

    def get_entities_schema(
        self, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(
            f"""
            .show databases entities with (showObfuscatedStrings=true)
            | where DatabaseName == '{database or self.config.database_name}'
            | project EntityName, EntityType, Folder, DocString
        """
        )

    def get_table_schema(
        self, table_name: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(f".show table {table_name} cslschema", database=database)

    def get_function_schema(
        self, function_name: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(f".show function {function_name}", database=database)

    def sample_table_data(
        self, table_name: str, sample_size: int = 10, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(f"{table_name} | sample {sample_size}", database=database)

    def sample_function_data(
        self,
        function_call_with_params: str,
        sample_size: int = 10,
        database: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self._execute(
            f"{function_call_with_params} | sample {sample_size}", database=database
        )

    def ingest_inline_into_table(
        self, table_name: str, data_comma_separator: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self._execute(
            f".ingest inline into table {table_name} <| {data_comma_separator}",
            database=database,
        )

    def _run_clear_streamingingestion_schema(
        self, database: Optional[str] = None
    ) -> None:
        self._execute(
            ".clear database cache streamingingestion schema",
            readonly_override=True,
            database=database,
        )

    def _execute(
        self,
        query: str,
        readonly_override: bool = False,
        database: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        caller_frame = inspect.currentframe().f_back  # type: ignore
        # Get the name of the caller function
        action = caller_frame.f_code.co_name  # type: ignore

        database = (
            database
            or self.config.database_name
            or cast(str, self.conn.client.default_database)  # type: ignore
        )
        # agents can send messy inputs
        database = database.strip()
        query = query.strip()

        client = self.conn.client
        crp: ClientRequestProperties = ClientRequestProperties()
        crp.application = f"kusto-mcp-server{{{__version__}}}"  # type: ignore
        crp.client_request_id = f"KMCP.{action}:{str(uuid.uuid4())}"  # type: ignore
        if action not in self.DESTRUCTIVE_TOOLS and not readonly_override:
            crp.set_option("request_readonly", True)
        result_set = client.execute(database, query, crp)
        return format_results(result_set)


assert os.environ.get(
    "KUSTO_SERVICE_URI"
), "Environment variable KUSTO_SERVICE_URI must be set."

# Create the service instance
service = KustoService(
    config=KustoConfig(
        query_service_uri=cast(str, os.environ.get("KUSTO_SERVICE_URI")),
        database_name=os.environ.get("KUSTO_DATABASE"),
    )
)

# Bind service methods directly as MCP tools
mcp.add_tool(
    service.execute_query,
    description="Executes a KQL query on specified database. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.execute_command,
    description="Executes a kusto management command on specified database. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(service.list_databases, description="Lists databases in the cluster.")
mcp.add_tool(
    service.list_tables,
    description="Lists tables in specified database. If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.get_entities_schema,
    description="Get the schema of all entities of a specific database; tables, materialized view, functions. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`",
)
mcp.add_tool(
    service.get_table_schema,
    description="Gets schema for a table in a database. If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.get_function_schema,
    description="Gets schema for a function in a database. Including the params and the output schema. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`",
)
mcp.add_tool(
    service.sample_table_data,
    description="Samples data from a table in database. If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.sample_function_data,
    description="Samples data from a function call in a database. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.ingest_inline_into_table,
    description="Ingests inline CSV data without column names into a table in a database. "
    "If database wasn't provided, will use env `KUSTO_DATABASE`.",
)
mcp.add_tool(
    service.print_file,
    description="Reads the first n lines from the specified absolute path. "
    "Set lines_number; use -1 to read the entire content.",
)
mcp.add_tool(
    service.ingest_csv_file_to_table,
    description="ingest csv file to an existing table and database using file abs path, if the table does not exist, "
    "create a table based on the csv's headers. If database wasn't provided, will use env `KUSTO_DATABASE`",
)
