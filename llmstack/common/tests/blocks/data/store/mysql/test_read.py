import unittest

from llmstack.common.blocks.data.store.mysql import MySQLConfiguration
from llmstack.common.blocks.data.store.mysql.read import MySQLReader, MySQLReaderInput


class MySQLReadTest(unittest.TestCase):
    def test_read(self):
        configuration = MySQLConfiguration(
            user="root",
            password="",
            host="localhost",
            port=5432,
            dbname="usersdb",
        )
        reader_input = MySQLReaderInput(
            sql="SELECT * FROM users",
        )

        response = MySQLReader().process(
            reader_input,
            configuration,
        )

        self.assertEqual(len(response.documents), 1)
