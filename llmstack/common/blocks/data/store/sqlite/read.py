import json
from collections import defaultdict

from llmstack.common.blocks.base.processor import ProcessorInterface
from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.constants import DatabaseType
from llmstack.common.blocks.data.store.sqlite import SQLiteConfiguration, SQLiteOutput
from llmstack.common.blocks.data.store.utils import get_sqlalchemy_database_connection


class SQLiteReaderInput(BaseSchema):
    sql: str


class SQLiteReader(
    ProcessorInterface[SQLiteReaderInput, SQLiteOutput, SQLiteConfiguration],
):
    def fetch_columns(self, columns):
        column_names = set()
        duplicates_counters = defaultdict(int)
        new_columns = []

        for col in columns:
            column_name = col[0]
            while column_name in column_names:
                duplicates_counters[col[0]] += 1
                column_name = "{}{}".format(
                    col[0],
                    duplicates_counters[col[0]],
                )

            column_names.add(column_name)
            new_columns.append(
                {"name": column_name, "friendly_name": column_name, "type": col[1]},
            )

        return new_columns

    def process(
        self,
        input: SQLiteReaderInput,
        configuration: SQLiteConfiguration,
    ) -> SQLiteOutput:
        connection = None
        try:
            connection = get_sqlalchemy_database_connection(DatabaseType.SQLITE, configuration.dict())
            result = connection.execute(input.sql)
            cursor = result.cursor

            if cursor.description is not None:
                columns = self.fetch_columns(
                    [(i[0], None) for i in cursor.description],
                )
                rows = [dict(zip((column["name"] for column in columns), row)) for row in cursor]

                data = {"columns": columns, "rows": rows}
                json_data = json.dumps(data)
            else:
                raise Exception("Query completed but it returned no data.")
        except Exception as e:
            if connection:
                connection.close()
                connection.engine.dispose()
            raise e
        finally:
            if connection:
                connection.close()
                connection.engine.dispose()
        return SQLiteOutput(
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
