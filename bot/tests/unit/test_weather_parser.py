import unittest
import os
import json
from bs4 import BeautifulSoup

from bot.weather_parser.weather import WeatherParser


class WeatherParserTest(unittest.TestCase):
    """Test weather_parser"""

    def setUp(self):

        # Load test data
        root_dir = os.path.dirname(os.path.abspath(__file__))
        test_data_file = os.listdir(os.path.join(root_dir, 'test_data'))
        self.test_three_hours_data = []
        self.test_seven_days_data = []
        for file_name in test_data_file:
            with open(os.path.join(root_dir, 'test_data', file_name),
                      'r', encoding='utf8') as fp:
                if file_name == 'three_hours.json':
                    self.test_three_hours_data.append(json.load(fp))
                elif file_name == 'seven_days.json':
                    self.test_seven_days_data.append(json.load(fp))

        # Convert every parsed_data to beautifulsoup format
        for test_data in self.test_three_hours_data:
            test_data['parsed_data'] = self.string_to_bs_format(
                test_data['parsed_data']
            )
        for test_data in self.test_seven_days_data:
            test_data['parsed_data'] = self.string_to_bs_format(
                test_data['parsed_data']
            )
        self.wea = WeatherParser()
        self.wea.approximate_matching(['台北', '大安'])

    def tearDown(self):
        self.wea = None

    def test_approximate_matching(self):
        """Test approximate mathcing"""

        self.assertEqual(self.wea.query[0], '臺北市')
        self.assertEqual(self.wea.query[1], '大安區')
        self.assertEqual(self.wea.county_code, '6300300')
        self.assertEqual(self.wea.station_id, 14)

    def test_request_weather(self):
        """Test weather website request function"""

        # Test three hour raw data successful
        three_hour_raw_data = (self.wea.request_weather(
            self.wea.three_hour_website
        ))
        self.assertIsNotNone(three_hour_raw_data)

        # Test seven day raw data successful
        seven_day_raw_data = (self.wea.request_weather(
            self.wea.seven_day_website
        ))
        self.assertIsNotNone(seven_day_raw_data)

        # Test air quality successful
        air_quality_raw_data = (self.wea.request_weather(
            self.wea.air_website
        ))
        self.assertIsNotNone(air_quality_raw_data)

    def test_parse_three_hours_data(self):
        """Test three hours data parse function"""

        for test_data in self.test_three_hours_data:
            three_hours_parsed_data = (self.wea.parse_three_hours_data(
                test_data['raw_data']
            ))
            self.assertDictEqual(three_hours_parsed_data,
                                 test_data['parsed_data'])

    def test_parse_seven_days_data(self):
        """Test seven days data parse function"""

        for test_data in self.test_seven_days_data:
            seven_days_parsed_data = (self.wea.parse_seven_days_data(
                test_data['raw_data']
            ))
            self.assertDictEqual(seven_days_parsed_data,
                                 test_data['parsed_data'])

    def test_three_hours_collect_data(self):
        """Test three hours collect data function"""

        for test_data in self.test_three_hours_data:
            three_hours_collect_data = (self.wea.collect_data(
                test_data['parsed_data']
            ))

            # Assertion of every day of collect data
            for day, ground in zip(three_hours_collect_data,
                                   test_data['collect_data']):
                self.assertDictEqual(day, ground)

    def test_seven_days_collect_data(self):
        """Test seven days collect data function"""

        for test_data in self.test_seven_days_data:
            seven_days_collect_data = (self.wea.collect_data(
                test_data['parsed_data']
            ))
            for day, ground in zip(seven_days_collect_data,
                                   test_data['collect_data']):
                self.assertDictEqual(day, ground)

    def test_get_colspan(self):
        """Test get_colspan function"""

        self.assertEqual(self.wea.get_colspan(5), 5)
        self.assertEqual(self.wea.get_colspan('10'), 10)
        self.assertEqual(self.wea.get_colspan(None), 1)
        self.assertEqual(self.wea.get_colspan(''), 1)

    def string_to_bs_format(self, parsed_data):
        """Convert BeautifulSoup format to string"""

        for key in parsed_data.keys():
            if key != 'col':
                parsed_data[key] = [BeautifulSoup(tag, 'html.parser').find()
                                    for tag in parsed_data[key]]
        return parsed_data
