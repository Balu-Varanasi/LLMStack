from enum import StrEnum
from typing import List

import sqlalchemy

from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.mysql import MySQLConfiguration
from llmstack.common.blocks.data.store.mysql import SSLMode as MySQLSSLMode
from llmstack.common.blocks.data.store.postgres import PostgresConfiguration
from llmstack.common.blocks.data.store.postgres import SSLMode as PostgresSSLMode
from llmstack.common.blocks.data.store.sqlite import SQLiteConfiguration


class DatabaseType(StrEnum):
    POSTGRESQL = "POSTGRESQL"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"


SSLMode = PostgresSSLMode | MySQLSSLMode

DatabaseConfiguration = MySQLConfiguration | PostgresConfiguration | SQLiteConfiguration


class DatabaseOutput(BaseSchema):
    documents: List[DataDocument]


def _get_ssl_config(type: DatabaseType, configuration: dict):
    ssl_config = {"sslmode": configuration.get("sslmode", "prefer")}

    # Create SSL configuration

    return ssl_config


def get_database_connection(
    type: DatabaseType,
    configuration: DatabaseConfiguration,
):
    ssl_config = (
        _get_ssl_config(
            type,
            configuration,
        )
        if configuration.get("use_ssl")
        else {}
    )

    # Create URL
    db_url = sqlalchemy.engine.url.URL(
        drivername=configuration["driver"],
        username=configuration["username"],
        password=configuration["password"],
        host=configuration["host"],
        port=configuration["port"],
        database=configuration["database_name"],
        connect_args=ssl_config,
    )

    # Create engine
    engine = sqlalchemy.create_engine(db_url)

    # Connect to the database
    connection = engine.connect()

    return connection
