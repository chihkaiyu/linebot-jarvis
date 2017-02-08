#!/usr/bin/env python3
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen

url = 'http://web.metro.taipei/c/2stainfo.asp'
rawData = urlopen(url)
tmp = BeautifulSoup(rawData, 'html.parser').find_all('optgroup', limit=5).find_all('option')


