from enum import StrEnum


class DatabaseType(StrEnum):
    POSTGRESQL = "POSTGRESQL"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"


DRIVERS: dict[DatabaseType, str] = {
    DatabaseType.POSTGRESQL: "postgresql",
    DatabaseType.MYSQL: "mysql+mysqlclient",
    DatabaseType.SQLITE: "sqlite",
}
