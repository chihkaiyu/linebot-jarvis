import unittest

from db_operator.db_operator import DBConnector


class DatabaseTest(unittest.TestCase):
    """For stupid test"""

    def setUp(self):
        mysql_login_info = {'user': 'test',
                            'password': 'yurabuai99',
                            'database': 'testLineBot',
                            'host': 'localhost'}
        self.db_conn = DBConnector(mysql_login_info)
        self.table_name = 'USER'
        self.userid_column = 'userID'
        self.favorite_column = 'favorite'
        self.last_cmd_column = 'lastCmd'

    def tearDown(self):
        self.db_conn.drop(self.table_name)
        self.db_conn = None

    def test_table_exists(self):
        """Test whether table exists, and test db_init"""

        self.assertEqual(False, self.db_conn.is_table(self.table_name))
        self.db_conn.db_init()
        self.assertEqual(True, self.db_conn.is_table(self.table_name))
