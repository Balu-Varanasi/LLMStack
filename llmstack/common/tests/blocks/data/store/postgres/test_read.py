import unittest

from llmstack.common.blocks.data.store.postgres import PostgresConfiguration
from llmstack.common.blocks.data.store.postgres.read import (
    PostgresReader,
    PostgresReaderInput,
)


class PostgresReadTest(unittest.TestCase):
    def test_read(self):
        configuration = PostgresConfiguration(
            user="root",
            password="",
            host="localhost",
            port=5432,
            dbname="usersdb",
        )
        reader_input = PostgresReaderInput(
            sql="SELECT * FROM users",
        )

        response = PostgresReader().process(
            reader_input,
            configuration,
        )

        self.assertEqual(len(response.documents), 1)
