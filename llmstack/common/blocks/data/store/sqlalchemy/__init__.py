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


def get_database_connection(
    type: DatabaseType,
    configuration: DatabaseConfiguration,
):
    from llmstack.common.blocks.data.store.mysql import get_mysql_ssl_config
    from llmstack.common.blocks.data.store.postgres import get_pg_ssl_config

    connect_args: dict = {}

    if configuration.get("use_ssl"):
        ssl_config = None
        if type == DatabaseType.POSTGRESQL:
            ssl_config = get_pg_ssl_config(configuration)
        elif type == DatabaseType.MYSQL:
            ssl_config = get_mysql_ssl_config(configuration)

        connect_args["ssl"] = ssl_config

    # Create URL
    db_url = sqlalchemy.engine.url.URL(
        drivername=configuration["driver"],
        username=configuration["username"],
        password=configuration["password"],
        host=configuration["host"],
        port=configuration["port"],
        database=configuration["database_name"],
    )

    # Create engine
    engine = sqlalchemy.create_engine(db_url, connect_args=connect_args)

    # Connect to the database
    connection = engine.connect()

    return connection
