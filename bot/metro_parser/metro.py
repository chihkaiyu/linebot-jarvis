#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import json
from urllib.request import urlopen

from bs4 import BeautifulSoup
from fuzzywuzzy import process


class MetroParser(object):
    """A class get metro information"""

    def __init__(self):

        # Get metor station code
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(root_dir, 'metro_code.json'),
                  'r', encoding='utf8') as fp:
            self.all_metro_code = json.load(fp)

    def approximat_matching(self, query):
        """Approximate matching for station name"""

        # Approximate matching
        query[0] = process.extractOne(query[0], self.all_metro_code.keys())[0]
        query[1] = process.extractOne(query[1], self.all_metro_code.keys())[0]
        self.query = query
        s1 = self.all_metro_code[query[0]]
        s2 = self.all_metro_code[query[1]]

        # Set request url
        metro_url = ('http://web.metro.taipei/c/2stainfo.asp?'
                     's1elect={STATION1}&action=query&s2elect={STATION2}'
                     '&submit=%C2%A0%E7%A2%BA%E5%AE%9A%C2%A0'
                     .format(STATION1=s1, STATION2=s2))
        return metro_url

    def request_metro(self, metro_url):
        """Send request to website"""

        raw_data = urlopen(metro_url)
        return raw_data

    def parsed_data(self, raw_data):
        """Filter the data we want"""

        # Filter data
        soup = BeautifulSoup(raw_data, 'html.parser')
        filtered = soup.find_all('div')

        # Parse data
        # all kind of prices at 4, 5, 6
        # duration and how-to-get-there at 11, 12
        parsed_data = {}
        parsed_data['prices'] = [kind.get_text() for kind in filtered[4:7]]
        parsed_data['duration'] = filtered[11].get_text()
        parsed_data['howto'] = filtered[12].get_text()
        return parsed_data

    def typesetting(self, parsed_data):
        """Combine the result in displaying format"""

        display = ('{STATION1} => {STATION2}\n'
                   '票價\n'
                   '單程票: {ONEWAY}\n'
                   '電子票證: {ELECTRIC}\n'
                   '敬老卡、愛心卡、愛心陪伴卡: {SPECIAL}\n'
                   '乘車時間: {DURATION}\n'
                   '乘車方式: {HOWTO}'
                   .format(STATION1=self.query[0], STATION2=self.query[1],
                           ONEWAY=parsed_data['prices'][0],
                           ELECTRIC=parsed_data['prices'][1],
                           SPECIAL=parsed_data['prices'][2],
                           DURATION=parsed_data['duration'],
                           HOWTO=parsed_data['howto']))
        return display
