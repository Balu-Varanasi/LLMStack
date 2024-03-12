import json

from llmstack.common.blocks.base.processor import ProcessorInterface
from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.sqlalchemy import (
    DatabaseConfiguration,
    DatabaseOutput,
    DatabaseType,
    get_database_connection,
)


class DatabaseReaderInput(BaseSchema):
    sql: str


class DatabaseReader(
    ProcessorInterface[DatabaseReaderInput, DatabaseOutput, DatabaseConfiguration],
):
    def fetch_columns(self, columns):
        raise NotImplementedError

    def process(
        self,
        input: DatabaseReaderInput,
        configuration: DatabaseConfiguration,
    ) -> DatabaseOutput:
        database_type = DatabaseType.POSTGRESQL
        connection = get_database_connection(database_type, configuration.dict())
        cursor = connection.cursor()
        try:
            cursor.execute(input.sql)
            if cursor.description is not None:
                # logic to fetch columns and rows
                data = {"columns": [], "rows": []}
                json_data = json.dumps(data)
            else:
                raise Exception("Query completed but it returned no data.")
        except Exception as e:
            connection.cancel()
            raise e
        return DatabaseOutput(
            documents=[
                DataDocument(
                    content=json_data,
                    content_text=json_data,
                    metadata={
                        "mime_type": "application/json",
                    },
                ),
            ],
        )
