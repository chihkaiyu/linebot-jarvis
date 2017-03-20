import unittest

from weatherParser import weather


class WeatherParserTest(unittest.TestCase):
    """WeatherParser test"""

    def setUp(self):
        self.command = ['台北', '大安']

    def test_stupid_test(self):
        """Definitely pass test"""
        self.assertEqual(True, True)
