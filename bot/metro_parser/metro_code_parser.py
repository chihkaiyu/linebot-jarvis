#!/usr/bin/env python3
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://web.metro.taipei/c/2stainfo.asp'
rawData = urlopen(url)
staCode = BeautifulSoup(rawData, 'html.parser').find('select').find_all('option')

# make sure we got unique key
d = {}
for sta in staCode:
    k = sta.get_text().split(' ')
    if k[0] not in d:
        d[k[0]] = sta['value']
    if k[1] not in d:
        d[k[1]] = sta['value']

f = open('metroCode.ini', 'w')
f.write('[station]\n')
for i in iter(d):
    f.write('{} = {}\n'.format(i, d[i]))
f.close()
