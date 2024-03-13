from enum import StrEnum
from typing import List

import sqlalchemy

from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.database.mysql import (
    MySQLConfiguration,
    get_mysql_ssl_config,
)
from llmstack.common.blocks.data.store.database.postgresql import (
    PostgresConfiguration,
    get_pg_ssl_config,
)
from llmstack.common.blocks.data.store.database.sqlite import SQLiteConfiguration


class DatabaseType(StrEnum):
    POSTGRESQL = "POSTGRESQL"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"


DRIVERS: dict[DatabaseType, str] = {
    DatabaseType.POSTGRESQL: "postgresql+psycopg2",
    DatabaseType.MYSQL: "mysql+mysqldb",
    DatabaseType.SQLITE: "sqlite+pysqlite",
}

DatabaseConfiguration = MySQLConfiguration | PostgresConfiguration | SQLiteConfiguration


class DatabaseOutput(BaseSchema):
    documents: List[DataDocument]


def get_sqlalchemy_database_connection(
    type: DatabaseType,
    configuration: DatabaseConfiguration,
    ssl_config: dict = None,
) -> sqlalchemy.engine.Connection:
    if type not in DRIVERS:
        raise ValueError(f"Unsupported database type: {type}")

    if not ssl_config:
        if type == DatabaseType.POSTGRESQL:
            ssl_config = get_pg_ssl_config(configuration.dict())
        elif type == DatabaseType.MYSQL:
            ssl_config = get_mysql_ssl_config(configuration.dict())

    driver_name = DRIVERS[type]

    if type == DatabaseType.SQLITE:
        database_name = configuration.dbpath
    else:
        database_name = configuration.dbname

    connect_args: dict = {}

    if ssl_config:
        connect_args["ssl"] = ssl_config

    # Create URL
    db_url = sqlalchemy.engine.URL.create(
        drivername=driver_name,
        username=configuration.user if hasattr(configuration, "user") else None,
        password=configuration.password if hasattr(configuration, "password") else None,
        host=configuration.host if hasattr(configuration, "host") else None,
        port=configuration.port if hasattr(configuration, "port") else None,
        database=database_name,
    )

    # Create engine
    engine = sqlalchemy.create_engine(db_url, connect_args=connect_args)

    # Connect to the database
    connection = engine.connect()

    return connection
