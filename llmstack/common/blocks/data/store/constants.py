from enum import StrEnum


class DatabaseType(StrEnum):
    POSTGRESQL = "POSTGRESQL"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"


DRIVERS: dict[DatabaseType, str] = {
    DatabaseType.POSTGRESQL: "postgresql+psycopg2",
    DatabaseType.MYSQL: "mysql+mysqldb",
    DatabaseType.SQLITE: "sqlite+pysqlite",
}
