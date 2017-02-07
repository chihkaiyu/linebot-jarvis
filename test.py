#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from weatherParser.weather import *

loca = ['台北', '大安']
res = getWeather(loca)
print res['date'][0].encode('utf-8')
