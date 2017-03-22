import unittest

from weather_parser.weather import WeatherParser

class WeatherParserTest(unittest.TestCase):
    """Test weather_parser"""

    def setUp(self):
        self.wea = WeatherParser(['台北', '大安'])
        with open('website_test_data/three_hours_1.htm',
                  'r', encoding='utf8') as fp:
            self.three_hours_raw_data = fp.read()
        with open('website_test_data/seven_days_1.htm',
                  'r', encoding='utf8') as fp:
            self.seven_days_raw_data = fp.read()

    def tearDown(self):
        self.wea = None

    def test_initialized_object(self):
        """Test initialized value of WeatherParser object"""

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

        three_hours_parsed_data = (self.wea.parse_three_hours_data(
            self.three_hours_raw_data
        ))
        self.assertEqual(sum(three_hours_parsed_data['col']), 17)
        self.assertEqual(len(three_hours_parsed_data['date']), 3)
        self.assertEqual(len(three_hours_parsed_data['time']), 17)
        self.assertEqual(len(three_hours_parsed_data['temp']), 17)
        self.assertEqual(len(three_hours_parsed_data['cond']), 17)

    def test_parse_seven_days_data(self):
        """Test seven days data parse function"""

        seven_days_parsed_data = (self.wea.parse_seven_days_data(
            self.seven_days_raw_data
        ))
        self.assertEqual(sum(seven_days_parsed_data['col']), 14)
        self.assertEqual(len(seven_days_parsed_data['date']), 7)
        self.assertEqual(len(seven_days_parsed_data['time']), 14)
        self.assertEqual(len(seven_days_parsed_data['temp']), 14)
        self.assertEqual(len(seven_days_parsed_data['cond']), 14)

    def test_three_hours_collect_data(self):
        """Test three hours collect data function"""

        three_hours_parsed_data = (self.wea.parse_three_hours_data(
            self.three_hours_raw_data
        ))
        three_hours_collect_data = (self.wea.collect_data(
            three_hours_parsed_data
        ))
        self.assertEqual(len(three_hours_collect_data), 3)

    def test_seven_days_collect_data(self):
        """Test seven days collect data function"""

        seven_days_parsed_data = (self.wea.parse_seven_days_data(
            self.seven_days_raw_data
        ))
        seven_days_collect_data = (self.wea.collect_data(
            seven_days_parsed_data
        ))
        self.assertEqual(len(seven_days_collect_data), 7)

    '''
    def test_air_quality(self):
        pass

    def test_typesetting(self):
        pass
    '''

    def test_get_colspan(self):
        """Test get_colspan function"""

        self.assertEqual(self.wea.get_colspan(5), 5)
        self.assertEqual(self.wea.get_colspan('10'), 10)
        self.assertEqual(self.wea.get_colspan(None), 1)
        self.assertEqual(self.wea.get_colspan(''), 1)


if __name__ == '__main__':
    unittest.main()
