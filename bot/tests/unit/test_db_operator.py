import unittest
import json
import os

from bot.db_operator.db_operator import DatabaseConnector
import mysql.connector

class DatabaseConnectorTest(unittest.TestCase):
    """Test database connector"""

    def setUp(self):

        mysql_login_info = {'user': 'test',
                            'password': 'yurabuai99',
                            'database': 'linebot',
                            'host': '127.0.0.1'}
        self.db_test = DatabaseConnector(mysql_login_info)

        # Load test database
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(root_dir, 'test_data', 'database_test.sql'),
                  'r', encoding='utf8') as fp:
            sql_file = fp.read()
        sql_file.replace('\n', ' ').split(';')
        for cmd in sql_file:
            try:
                self.db_test.cursor.execute(cmd)
            except mysql.connector.errors.OperationalError:
                print('Command skipped: {}')

    def tearDown(self):
        self.db_test = None

    def test_is_record(self):
        """Test whether a record exists"""

        table_name = 'USER'
        column = 'userID'
        target = 'test'
        self.assertFalse(self.db_test.is_record(table_name, column, target))
        self.db_test.cursor.execute('')
        pass

    def test_is_table(self):
        pass

    def test_query(self):
        pass

    def test_insert(self):
        pass

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_init(self):
        pass
