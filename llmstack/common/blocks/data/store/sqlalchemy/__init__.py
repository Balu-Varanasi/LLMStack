from typing import List

import sqlalchemy

from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.mysql import MySQLConfiguration
from llmstack.common.blocks.data.store.postgres import PostgresConfiguration
from llmstack.common.blocks.data.store.sqlite import SQLiteConfiguration

from ..constants import DRIVERS, DatabaseType

DatabaseConfiguration = MySQLConfiguration | PostgresConfiguration | SQLiteConfiguration


class DatabaseOutput(BaseSchema):
    documents: List[DataDocument]


def get_database_connection(
    type: DatabaseType,
    configuration: DatabaseConfiguration,
):
    if type not in DRIVERS:
        raise ValueError(f"Unsupported database type: {type}")

    connect_args: dict = {}

    if configuration.get("use_ssl"):
        ssl_config = None
        if type == DatabaseType.POSTGRESQL:
            from llmstack.common.blocks.data.store.postgres import get_pg_ssl_config

            ssl_config = get_pg_ssl_config(configuration)
        elif type == DatabaseType.MYSQL:
            from llmstack.common.blocks.data.store.mysql import get_mysql_ssl_config

            ssl_config = get_mysql_ssl_config(configuration)

        connect_args["ssl"] = ssl_config

    # Create URL
    db_url = sqlalchemy.engine.url.URL(
        drivername=DRIVERS[type],
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
