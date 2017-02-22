#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from configparser import ConfigParser
import os
import json
import math

def findNearest(s, f):
    # load longtitude and latitude of query dist.
    county = ConfigParser()
    county.read(os.path.join(parDir, 'countyLongLat.ini'), encoding='utf8')
    coordinate = county[location[0]][location[1]].split()
    lat, lon = int(coordinate[0]), int(coordinate[1])
    defCounty = ConfigParser()
    defCounty.read(os.path.join(parDir))




def getWeather(location):
    # get weather
    conf = ConfigParser()
    parDir = os.path.dirname(os.path.abspath(__file__))
    conf.read(os.path.join(parDir, 'countyCode.ini'), encoding='utf8')
    rawData = (urlopen('http://www.cwb.gov.tw/V7/forecast/town368/3Hr/{}.htm'.
            format(conf[location[0]][location[1]])))
    
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
    res = json.loads(rawData.read().decode('utf8'))['Data']

    # check query dist whether in default county
    defCounty = ConfigParser()
    defCounty.read(os.path.join(parDir, 'defCountyLongLat.ini'), encoding='utf8')
    if not defCounty.has_option(location[0], location[1]):
        # caculate distance between all location in defCountyLongLat.ini
        # find out the nearest district, and use it as result.
        # load longtitude and latitude of query dist.
        county = ConfigParser()
        county.read(os.path.join(parDir, 'countyLongLat.ini'), encoding='utf8')
        coordinate = county[location[0]][location[1]].split()
        lamS, phiS = float(coordinate[0]), float(coordinate[1])

        # calculate distance of every station in the same county
        min = 1000
        for dist in defCounty.items(location[0]):
            tmp = dist[1].split()
            lamF, phiF = float(tmp[0]), float(tmp[1])
            deltaPhi = abs(phiS-phiF)
            deltaLam = abs(lamS-lamF)
            deltaLo = 2*math.asin(math.sqrt(math.sin(deltaPhi/2)**2+math.cos(phiS)*math.cos(phiF)*math.sin(deltaLam/2)**2))
            if deltaLo < min:
                min = deltaLo
                site = dist[0]
    else:
        site = location[1]

    # get obeservation data
    for dist in res:
        if site == dist['SiteName']:
            # site = dist['SiteName']
            aqi = dist['AQI']
            aqiStyle = dist['AQIStyle']
            break;

    # delete this after done all feature
    '''
    #================================#
    if not aqi:
        site = 'Can not find this district.'
        aqi = 'Can not find this district.'
        aqiStyle = 'Can not find this district.'
    #================================#
    '''

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
    display = ''.join(location) + '\n'
    display += '空氣品質：\n'
    display += '    觀測站: ' + site + '\n'
    display += '    AQI: ' + aqi + '\n'
    display += '    空氣品質指標： ' + aqiStyle + '\n'
    display += ''.join(date[0]) + '\n'
    display += '    時間    ' + '溫度   ' + '降雨機率' + '\n'
    for i in range(numCol):
        display += '    ' + time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'
    if numCol != 8:
        display += ''.join(date[1]) + '\n'
        display += '    時間    ' + '溫度   ' '降雨機率' + '\n'
        for i in range(numCol ,8):
            display += '    ' + time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'

    return display

if __name__ == '__main__':
    location = ['雲林', '斗南']
    print(getWeather(location))

'''
    # typesetting result
    display = ''.join(location) + '\n'
    display += '空氣品質：\n'
    display += '    AQI: ' + aqi + '\n'
    display += '    空氣品質指標： ' + aqiStyle + '\n'
    display += ''.join(date[0]) + '\n'
    display += '時間    ' + '溫度   ' + '降雨機率' + '\n'
    for i in range(numCol):
        display += time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'
    if numCol != 8:
        display += ''.join(date[1]) + '\n'
        display += '時間    ' + '溫度   ' '降雨機率' + '\n'
        for i in range(numCol ,8):
            display += time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'
'''
