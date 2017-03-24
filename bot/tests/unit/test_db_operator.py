import unittest
import json

from bot.db_operator.db_operator import DatabaseConnector


class DatabaseConnectorTest(unittest.TestCase):
    """Test database connector"""

    def setUp(self):

        mysql_login_info = {'user': 'bot',
                            'password': 'yurabuai99',
                            'database': 'linebot',
                            'host': 'db'}
        self.db_test = DatabaseConnector(mysql_login_info)

    def tearDown(self):
        self.db_test = None

    def test_initilized_value(self):
        pass

    def test_is_record(self):
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
