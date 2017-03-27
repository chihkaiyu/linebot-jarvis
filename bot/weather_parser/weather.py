#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is a module to get weather condition"""

from urllib.request import urlopen
import os
import json

from bs4 import BeautifulSoup
from fuzzywuzzy import process


class WeatherParser(object):
    """A class get weather condition, and parse data"""

    def __init__(self, query):
        # Preprocess
        query[0] = query[0].replace('台', '臺')
        query[1] = query[1].replace('台', '臺')

        # Get county code
        # root_dir = os.environ.get('ROOT_DIR')
        folder_name = os.path.dirname(os.path.abspath(__file__))
        code_file_path = os.path.join(folder_name, 'dist_info.json')
        code_file = json.load(open(code_file_path, 'r', encoding='utf8'))

        # Approximate matching
        query[0] = process.extractOne(query[0], code_file.keys())[0]
        query[1] = process.extractOne(query[1], code_file[query[0]].keys())[0]
        self.query = query
        self.county_code = code_file[query[0]][query[1]]['code']

        # Attribute
        self.three_hour_website = ('http://www.cwb.gov.tw/V7/forecast/town368'
                                   '/3Hr/{county_code}.htm'
                                   .format(county_code=self.county_code))
        self.seven_day_website = ('http://www.cwb.gov.tw/V7/forecast/town368'
                                  '/7Day/{county_code}.htm'
                                  .format(county_code=self.county_code))
        self.air_website = ('http://taqm.epa.gov.tw/taqm/aqs.ashx?'
                            'lang=tw&act=aqi-epa')
        self.station_id = int(code_file[query[0]][query[1]]['station_id'])

    def request_weather(self, url):
        """Send request to website"""

        raw_data = urlopen(url)
        return raw_data

    def parse_three_hours_data(self, raw_data):
        """Filter out the data we want"""

        # Filter data
        soup = BeautifulSoup(raw_data, 'html.parser')
        filtered = soup.find_all('tr')

        # Parse data
        # three hours
        # date: 0, time: 1, temperature: 3, rainfall prob.: 8
        parsed = {}
        parsed['date'] = filtered[0].find_all('td')[1:]
        parsed['col'] = [self.get_colspan(col.get('colspan'))
                         for col in parsed['date']]
        parsed['time'] = filtered[1].find_all('td')[1:]
        parsed['temp'] = filtered[3].find_all('td')[1:]

        # Duplicate rainfall prob.
        parsed['cond'] = []
        for rain in filtered[8].find_all('td')[1:]:
            if rain.get('colspan'):
                parsed['cond'].extend([rain, rain])
            else:
                parsed['cond'].append(rain)
        return parsed

    def parse_seven_days_data(self, raw_data):
        """Filter out the data we want"""

        # Filter data
        soup = BeautifulSoup(raw_data, 'html.parser')
        filtered = soup.find_all('tr')

        # Parse data
        # seven days
        # date: 0, time: 1, high temp: 3, low temp: 4, condition: 2
        parsed = {}
        parsed['date'] = filtered[0].find_all('td')[1:]
        parsed['col'] = [2]*7
        parsed['time'] = filtered[1].find_all('td')[1:]

        # Concatenate lowest and highest temperature
        parsed['temp'] = filtered[4].find_all('td')[1:]
        for low, high in zip(parsed['temp'],
                             filtered[3].find_all('td')[1:]):
            low.string = '{LOW}~{HIGH}'.format(LOW=low.get_text(),
                                               HIGH=high.get_text())
            # low.append('~{}'.format(high.get_text()))

        # Insert condition title to tag
        parsed['cond'] = filtered[2].find_all('img')
        for item in parsed['cond']:
            item.append(item['title'])
        return parsed

    def collect_data(self, parsed):
        """Put the data of a day into dictionary"""

        res = []
        start = 0
        for day, col in zip(parsed['date'], parsed['col']):
            end = start + col
            tmp_date = day.get_text()
            res.append({'col': col,
                        'date': '{WEEK} {DATE}'
                                .format(WEEK=tmp_date[:5], DATE=tmp_date[5:]),
                        'time': [time.get_text()
                                 for time in parsed['time'][start:end]],
                        'temp': [temp.get_text()
                                 for temp in parsed['temp'][start:end]],
                        'cond': [cond.get_text()
                                 for cond in parsed['cond'][start:end]]})
            start += col
        return res

    def air_quality(self, raw_data):
        """Get air quality, return formatted string"""
        aqi_data = json.loads(raw_data.read().decode('utf8'))['Data']
        res = {'aqiStyle': aqi_data[self.station_id]['AQIStyle'],
               'site': aqi_data[self.station_id]['SiteName']}
        if res['aqiStyle'] == 'AQI0':
            res['aqiStyle'] = '設備維護'
        elif res['aqiStyle'] == 'AQI1':
            res['aqiStyle'] = '良好'
        elif res['aqiStyle'] == 'AQI2':
            res['aqiStyle'] = '普通'
        elif res['aqiStyle'] == 'AQI3':
            res['aqiStyle'] = '對敏感族群不健康'
        elif res['aqiStyle'] == 'AQI4':
            res['aqiStyle'] = '對所有族群不健康'
        elif res['aqiStyle'] == 'AQI5':
            res['aqiStyle'] = '非常不健康'
        elif res['aqiStyle'] == 'AQI6':
            res['aqiStyle'] = '危害'
        display = ('空氣品質: \n'
                   '    觀測站: {site}\n'
                   '    空氣品質指標: {quality}\n'
                   .format(site=res['site'], quality=res['aqiStyle']))
        return display

    def typesetting(self, res, title=''):
        """Combine the result in displaying format"""

        # '    時間    溫度     降雨機率\n'
        display = ''
        for day in res:
            display += ('{D}\n'.format(D=day['date']) + title)
            for time, temp, rain in (zip(day['time'], day['temp'],
                                         day['cond'])):
                display += ('    {TIME}   {TEMP}       {RAIN}\n'
                            .format(TIME=time, TEMP=temp, RAIN=rain))
        return display

    def get_colspan(self, col):
        """Get number of column"""

        if col:
            return int(col)
        else:
            return 1

if __name__ == '__main__':
    import pprint
    COMMAND = ['台中', '豐原市']
    W = WeatherParser(COMMAND)
    three_hour_raw_data = W.request_weahter(W.three_hour_website)
    three_hour_parsed_data = W.parse_three_hours_data(three_hour_raw_data)
    three_hour_collect = W.collect_data(three_hour_parsed_data)
    three_hour_display = W.typesetting(three_hour_collect[:2],
                                       '    時間    溫度     降雨機率\n')
    seven_day_raw_data = W.request_weahter(W.seven_day_website)
    seven_day_parsed_data = W.parse_seven_days_data(seven_day_raw_data)
    seven_day_collect = W.collect_data(seven_day_parsed_data)
    seven_day_display = W.typesetting(seven_day_collect[1:])
    #pprint.pprint(three_hour_collect)

    air_raw_data = W.request_weahter(W.air_website)
    air_data = W.air_quality(air_raw_data)
    print(air_data)
    print(three_hour_display)
    print(seven_day_display)

