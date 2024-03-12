import sqlalchemy

from llmstack.common.blocks.data.store.mysql import MySQLConfiguration
from llmstack.common.blocks.data.store.postgres import PostgresConfiguration
from llmstack.common.blocks.data.store.sqlite import SQLiteConfiguration

from .constants import DRIVERS, DatabaseType

DatabaseConfiguration = MySQLConfiguration | PostgresConfiguration | SQLiteConfiguration


def get_sqlalchemy_database_connection(
    type: DatabaseType,
    configuration: DatabaseConfiguration,
    ssl_config: dict = None,
) -> sqlalchemy.engine.Connection:
    if type not in DRIVERS:
        raise ValueError(f"Unsupported database type: {type}")

    driver_name = DRIVERS[type]

    if type == DatabaseType.SQLITE:
        database_name = configuration.get("dbpath")
    else:
        database_name = configuration.get("dbname")

    connect_args: dict = {}

    if ssl_config:
        connect_args["ssl"] = ssl_config

    # Create URL
    db_url = sqlalchemy.engine.URL.create(
        drivername=driver_name,
        username=configuration.get("user"),
        password=configuration.get("password"),
        host=configuration.get("host"),
        port=configuration.get("port"),
        database=database_name,
    )

    # Create engine
    engine = sqlalchemy.create_engine(db_url, connect_args=connect_args)

    # Connect to the database
    connection = engine.connect()

    return connection
