#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from configparser import ConfigParser
import os
import json
#import fuzzywuzzy
from fuzzywuzzy import process


def getWeather(query):
    # replace 台 to 臺
    query[0] = query[0].replace('台', '臺')
    query[1] = query[1].replace('台', '臺')

    ## get weather
    parDir = os.path.dirname(os.path.abspath(__file__))
    conf = json.load(open(os.path.join(parDir, 'distInfo.json'), 'r', encoding='utf8'))
    # approximate matching
    query[0] = process.extractOne(query[0], conf.keys())[0]
    query[1] = process.extractOne(query[1], conf[query[0]].keys())[0]
    countyCode = conf[query[0]][query[1]][0]
    rawData = (urlopen('http://www.cwb.gov.tw/V7/forecast/town368/3Hr/{countyCode}.htm'.
            format(countyCode=countyCode)))
    
    soup = BeautifulSoup(rawData, 'html.parser')
    divided = soup.find_all('tr')
    
    # parse date at 0
    tmp = divided[0].find_all('td', limit=3)
    date = []
    date.append(tmp[1].get_text())
    if tmp[1].get('colspan'):
        numCol = int(tmp[1]['colspan'])
        if numCol != 8:
            date.append(tmp[2].get_text())
    else:
        numCol = 1
        date.append(tmp[2].get_text())

    # parse time at 1
    time = ['0']*8
    tmp = divided[1].find_all('span', limit=8)
    for i in range(8):
        time[i] = tmp[i].get_text()

    # parse temperature at 3
    temp = [0]*8
    tmp = divided[3].find_all('td', limit=9)
    for i in range(1, 9):
        temp[i-1] = tmp[i].get_text()

    # parse rainfall prob. at 8
    rainprob = []
    tmp = divided[8].find_all('td')
    if tmp[1].get('colspan'):
        for i in range(1, 5):
            rainprob.append(tmp[i].get_text())
            rainprob.append(tmp[i].get_text())
    else:
        rainprob.append(tmp[1].get_text())
        for i in range(2, 5):
            rainprob.append(tmp[i].get_text())
            rainprob.append(tmp[i].get_text())
        rainprob.append(tmp[5].get_text())

    # get AQI
    # http://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa
    rawData = urlopen('http://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa')
    stationID = int(conf[query[0]][query[1]][1])
    res = json.loads(rawData.read().decode('utf8'))['Data']
    aqi = res[stationID]['AQI']
    aqiStyle = res[stationID]['AQIStyle']
    site = res[stationID]['SiteName']

    if aqiStyle == 'AQI0':
        aqiStyle = '設備維護'
    elif aqiStyle == 'AQI1':
        aqiStyle = '良好'
    elif aqiStyle == 'AQI2':
        aqiStyle = '普通'
    elif aqiStyle == 'AQI3':
        aqiStyle = '對敏感族群不健康'
    elif aqiStyle == 'AQI4':
        aqiStyle = '對所有族群不健康'
    elif aqiStyle == 'AQI5':
        aqiStyle = '非常不健康'
    elif aqiStyle == 'AQI6':
        aqiStyle = '危害'

    # typesetting result
    display = ('{queryDist}\n'
                '空氣品質: \n'
                '    觀測站: {site}\n'
                '    AQI: {aqi}\n'
                '    空氣品質指標: {quality}\n'
                '{d}\n'
                '    時間    溫度   降雨機率\n'
                .format(queryDist=' '.join(query), site=site, aqi=aqi, quality=aqiStyle,
                        d='{} {}'.format(date[0][:5], date[0][5:])))

    for i in range(numCol):
        display += ('    {time}  {temp}     {rain}\n'
                    .format(time=time[i], temp=temp[i], rain=rainprob[i]))
    if numCol != 8:
        display += ('{date} {day}\n'
                    '    時間    溫度   降雨機率\n'
                    .format(date=date[1][:5], day=date[1][5:]))
        for i in range(numCol ,8):
            display += ('    {time}  {temp}     {rain}\n'
                        .format(time=time[i], temp=temp[i], rain=rainprob[i]))

    return display

if __name__ == '__main__':
    query = ['台中', '豐原市']
    print(getWeather(query))
