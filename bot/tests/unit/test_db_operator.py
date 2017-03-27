import unittest
import json
import os

from bot.db_operator.db_operator import DatabaseConnector
import mysql.connector


class DatabaseConnectorTest(unittest.TestCase):
    """Test database connector"""

    def setUp(self):

        mysql_login_info = {'user': 'bot',
                            'password': 'yurabuai99',
                            'database': 'linebot',
                            'host': '127.0.0.1'}
        self.db_test = DatabaseConnector(mysql_login_info)

        # will creat repeat database, have to fix it
        # Load test database
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(root_dir, 'test_data', 'database_test.sql'),
                  'r', encoding='utf8') as fp:
            sql_file = fp.read()
        sql_script = sql_file.replace('\n', '').split(';')
        for cmd in sql_script:
            self.db_test.cursor.execute(cmd)

    def tearDown(self):
        self.db_test = None

    def test_is_record(self):
        """Test whether a record exists"""

        table_name = 'USER'
        column = 'userID'
        false_target = 'notexists'
        true_target = 'test'

        self.assertFalse(self.db_test.is_record(table_name, column,
                                                false_target))
        self.assertTrue(self.db_test.is_record(table_name, column,
                                               true_target))

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
        true_condition = 'userID = \'test\''
        false_condition = 'userID = \'notexists\''

        self.assertEqual(self.db_test.query(table_name, true_column,
                                            true_condition), [('lion')])
        self.assertEqual(self.db_test.query(table_name, true_column,
                                            false_condition), [])

    def test_insert(self):
        """Test inserting database"""

        table_name = 'USER'
        data = {'userID': 'testingid', 'favorite': 'testlion',
                'lastCmd': 'I like lion very much'}
        self.db_test.insert(table_name, data)
        test_select_cmd = ('SELECT * FROM USER'
                           'WHERE userID=\'testingid\'')

        # True assertion
        self.db_test.cursor.execute(test_select_cmd)
        res = self.db_test.cursor.fetchall()
        self.assertEqual(res,
                         [('testingid', 'testlion', 'I like lion very much')])
        # False assertion
        delete_test_record = ('DELETE FROM USER'
                              'WHERE userID=\'testingid\'')
        self.db_test.cursor.execute(delete_test_record)
        self.db_test.cursor.execute(test_select_cmd)
        res = self.db_test.cursor.fetchall()
        self.assertEqual(res, [])

    def test_create(self):
        """Test create table database"""

        true_table_name = 'USER'
        false_table_name = 'notexists'
        self.assertTrue(self.db_test.is_table(true_table_name))
        self.assertFalse(self.db_test.is_table(false_table_name))

    def test_update(self):
        """Update in database"""

        table_name = 'USER'
        update_data = {'favorite': 'anan', 'lastCmd': 'I love kitty'}
        condition = 'userID=\'test_update\''
        test_update_record = ('INSERT INTO USER'
                              '(userID, favorite, lastCmd)'
                              'VALUES'
                              '(\'test_update\', \'haha\', \'I love lion\')')
        # Insert for test
        self.db_test.cursor.execute(test_update_record)
        self.db_test.update(table_name, update_data, condition)
        self.db_test.cursor.execute('SELECT * FROM USER'
                                    'WHERE userID=\'test_update\'')
        res = self.db_test.cursor.fetchall()
        self.assertEqual(res, [('test_update', 'anan', 'I love kieey')])

        # Delete test record
        delete_test_record = ('DELETE FROM USER'
                              'WHERE userID=\'test_update\'')
        self.db_test.cursor.execute(delete_test_record)
    '''
    def test_init(self):
        pass
    '''
