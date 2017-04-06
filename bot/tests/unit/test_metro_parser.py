import os
import json
import unittest

from bot.metro_parser.metro import MetroParser

class MetroParserTest(unittest.TestCase):
    """Test metro parser"""

    def setUp(self):
        self.metro_parser = MetroParser()
        self.query = ['六張離', '頭前莊']

        # Load test data
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(root_dir, 'test_data', 'metro_test_data.json'),
                  'r', encoding='utf8') as fp:
            self.test_data = json.load(fp)

    def tearDown(self):
        del self.metro_parser
        del self.test_data

    def test_approximate_matching(self):
        """Test approximate matching"""

        url = self.metro_parser.approximate_matching(self.query)
        self.assertEqual(url, self.test_data['url'])
        self.assertEqual(self.query[0], self.test_data['query'][0])
        self.assertEqual(self.query[1], self.test_data['query'][1])

    def test_request_metro(self):
        """Test metro website request function"""

        raw_data = self.metro_parser.request_metro(self.test_data['url'])
        self.assertIsNotNone(raw_data)

    def test_parsed_data(self):
        """Test parse metro data"""

        parsed_data = self.metro_parser.parsed_data(self.test_data['raw_data'])
        self.assertDictEqual(parsed_data, self.test_data['parsed_data'])

    def test_typesetting(self):
        """Test metro data typesetting"""

        self.metro_parser.query = self.test_data['query']
        display = self.metro_parser.typesetting(self.test_data['parsed_data'])
        self.assertEqual(display, self.test_data['display'])

