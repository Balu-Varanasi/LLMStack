import json
import logging
from typing import Dict, List, Optional

from pydantic import Field

from llmstack.common.blocks.base.schema import BaseSchema as _Schema
from llmstack.common.blocks.data.store.database.database_reader import (
    DatabaseReader,
    DatabaseReaderInput,
)
from llmstack.common.blocks.data.store.database.mysql import MySQLConfiguration
from llmstack.common.blocks.data.store.database.sqlalchemy import DatabaseType
from llmstack.common.blocks.data.store.vectorstore import Document
from llmstack.common.utils.models import Config
from llmstack.datasources.handlers.datasource_processor import (
    DataSourceEntryItem,
    DataSourceProcessor,
    DataSourceSchema,
)
from llmstack.datasources.models import DataSource

logger = logging.getLogger(__name__)


class MySQLConnection(_Schema):
    host: str = Field(description="Host of the MySQL instance")
    port: int = Field(
        description="Port number to connect to the MySQL instance",
    )
    database_name: str = Field(description="MySQL database name")
    username: str = Field(description="MySQL username")
    password: Optional[str] = Field(description="MySQL password")


class MySQLDatabaseSchema(DataSourceSchema):
    connection: Optional[MySQLConnection] = Field(
        description="MySQL connection details",
    )


class MySQLConnectionConfiguration(Config):
    config_type = "mysql_connection"
    is_encrypted = True
    mysql_config: Optional[Dict]


class MySQLDataSource(DataSourceProcessor[MySQLDatabaseSchema]):
    # Initializer for the class.
    # It requires a datasource object as input, checks if it has a 'data'
    # configuration, and sets up Weaviate Database Configuration.
    def __init__(self, datasource: DataSource):
        self.datasource = datasource
        if self.datasource.config and "data" in self.datasource.config:
            config_dict = MySQLConnectionConfiguration().from_dict(
                self.datasource.config,
                self.datasource.profile.decrypt_value,
            )
            self._configuration = MySQLDatabaseSchema(
                **config_dict["mysql_config"],
            )
            self._reader_configuration = MySQLConfiguration(
                user=self._configuration.connection.username,
                password=self._configuration.connection.password,
                host=self._configuration.connection.host,
                port=self._configuration.connection.port,
                dbname=self._configuration.connection.database_name,
                use_ssl=False,
            )
            self._source_name = self.datasource.name

    @staticmethod
    def name() -> str:
        return "MySQL"

    @staticmethod
    def slug() -> str:
        return "mysql"

    @staticmethod
    def description() -> str:
        return "Connect to a MySQL database"

    # This static method takes a dictionary for configuration and a DataSource object as inputs.
    # Validation of these inputs is performed and a dictionary containing the
    # MySQL Connection Configuration is returned.
    @staticmethod
    def process_validate_config(
        config_data: dict,
        datasource: DataSource,
    ) -> dict:
        return MySQLConnectionConfiguration(
            mysql_config=config_data,
        ).to_dict(
            encrypt_fn=datasource.profile.encrypt_value,
        )

    # This static method returns the provider slug for the datasource
    # connector.
    @staticmethod
    def provider_slug() -> str:
        return "mysql"

    def validate_and_process(self, data: dict) -> List[DataSourceEntryItem]:
        raise NotImplementedError

    def get_data_documents(self, data: dict) -> List[Document]:
        raise NotImplementedError

    def add_entry(self, data: dict) -> Optional[DataSourceEntryItem]:
        raise NotImplementedError

    def similarity_search(self, query: str, **kwargs) -> List[dict]:
        mysql_client = DatabaseReader()
        result = (
            mysql_client.process(
                DatabaseReaderInput(
                    type=DatabaseType.MYSQL,
                    sql=query,
                ),
                configuration=self._reader_configuration,
            )
            .documents[0]
            .content_text
        )
        json_result = json.loads(result)
        # JSON to csv
        csv_result = ""
        for row in json_result["rows"]:
            csv_result += (
                ",".join(
                    list(
                        map(
                            lambda entry: str(entry),
                            row.values(),
                        ),
                    ),
                )
                + "\n"
            )
        return [
            Document(
                page_content_key="content",
                page_content=csv_result,
                metadata={
                    "score": 0,
                    "source": self._source_name,
                },
            ),
        ]

    def hybrid_search(self, query: str, **kwargs) -> List[dict]:
        mysql_client = DatabaseReader()
        result = (
            mysql_client.process(
                DatabaseReaderInput(
                    type=DatabaseType.MYSQL,
                    sql=query,
                ),
                configuration=self._reader_configuration,
            )
            .documents[0]
            .content_text
        )
        json_result = json.loads(result)
        # JSON to csv
        csv_result = ""
        for row in json_result["rows"]:
            csv_result += (
                ",".join(
                    list(
                        map(
                            lambda entry: str(entry),
                            row.values(),
                        ),
                    ),
                )
                + "\n"
            )

        return [
            Document(
                page_content_key="content",
                page_content=csv_result,
                metadata={
                    "score": 0,
                    "source": self._source_name,
                },
            ),
        ]

    def delete_entry(self, data: dict) -> None:
        raise NotImplementedError

    def resync_entry(self, data: dict) -> Optional[DataSourceEntryItem]:
        raise NotImplementedError

    def delete_all_entries(self) -> None:
        raise NotImplementedError

    def get_entry_text(self, data: dict) -> str:
        return None, self._configuration.json()
