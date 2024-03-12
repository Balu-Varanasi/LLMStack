import datetime
import json
from collections import defaultdict

from llmstack.common.blocks.base.processor import ProcessorInterface
from llmstack.common.blocks.base.schema import BaseSchema
from llmstack.common.blocks.data import DataDocument
from llmstack.common.blocks.data.store.mysql import (
    MySQLConfiguration,
    MySQLOutput,
    get_mysql_connection,
)


class MySQLReaderInput(BaseSchema):
    sql: str


types_map = {
    0: "float",
    1: "integer",
    2: "integer",
    3: "integer",
    4: "float",
    5: "float",
    7: "datetime",
    8: "integer",
    9: "integer",
    10: "date",
    12: "datetime",
    15: "string",
    16: "integer",
    246: "float",
    253: "string",
    254: "string",
}


class MySQLJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(MySQLJSONEncoder, self).default(obj)


class MySQLReader(
    ProcessorInterface[MySQLReaderInput, MySQLOutput, MySQLConfiguration],
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
        input: MySQLReaderInput,
        configuration: MySQLConfiguration,
    ) -> MySQLOutput:
        connection = get_mysql_connection(configuration.dict())
        cursor = connection.cursor()
        try:
            cursor.execute(input.sql)
            if cursor.description is not None:
                columns = self.fetch_columns(
                    [(i[0], types_map.get(i[1], None)) for i in cursor.description],
                )
                rows = [dict(zip((column["name"] for column in columns), row)) for row in cursor]

                data = {"columns": columns, "rows": rows}
                json_data = json.dumps(data, cls=MySQLJSONEncoder)
            else:
                raise Exception("Query completed but it returned no data.")
        except Exception as e:
            connection.cancel()
            raise e
        return MySQLOutput(
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
