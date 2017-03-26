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
        sql_script = sql_file.replace('\n', '').split(';')
        for cmd in sql_script:
            try:
                self.db_test.cursor.execute(cmd)
            except mysql.connector.errors.OperationalError:
                print('Command skipped: ')

    def tearDown(self):
        self.db_test = None

    def test_is_record(self):
        """Test whether a record exists"""

        table_name = 'USER'
        column = 'userID'
        false_target = 'notexists'
        true_target = 'test'

        self.assertFalse(self.db_test.is_record(table_name, column, false_target))
        self.assertTrue(self.db_test.is_record(table_name, column, true_target))

    def test_is_table(self):
        """Test whether a table exists"""

        false_table_name = 'notexists'
        true_table_name = 'USER'

        self.assertFalse(self.db_test.is_table(false_table_name))
        self.assertTrue(self.db_test.is_table(true_table_name))

    def test_query(self):
        """Test querying database"""

        table_name = 'USER'
        true_column = ['favorite']
        # false_column = ['notexists']
        true_condition = 'userID = \'test\''
        # false_condition = 'userID = \'notexists\''

        self.assertEqual(self.db_test.query(table_name, true_column,
                                            true_condition), [('lion')])

    def test_insert(self):
        pass

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_init(self):
        pass
