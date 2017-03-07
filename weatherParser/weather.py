#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from configparser import ConfigParser
import os
import json
from fuzzywuzzy import process


def getWeather(query):
    # preprocess
    # replace 台 to 臺
    query[0] = query[0].replace('台', '臺')
    query[1] = query[1].replace('台', '臺')

    # get weather
    # load county code file
    parDir = os.path.dirname(os.path.abspath(__file__))
    conf = json.load(open(os.path.join(parDir, 'distInfo.json'), 'r', encoding='utf8'))

    # approximate matching
    query[0] = process.extractOne(query[0], conf.keys())[0]
    query[1] = process.extractOne(query[1], conf[query[0]].keys())[0]
    countyCode = conf[query[0]][query[1]][0]


    # get 3 hours result
    rawData = (urlopen('http://www.cwb.gov.tw/V7/forecast/town368/3Hr/{countyCode}.htm'.
            format(countyCode=countyCode)))
    soup = BeautifulSoup(rawData, 'html.parser')
    threeHour = soup.find_all('tr')

    rawData = (urlopen('http://www.cwb.gov.tw/V7/forecast/town368/7Day/{countyCode}.htm'.
            format(countyCode=countyCode)))
    soup = BeautifulSoup(rawData, 'html.parser')
    sevenDay = soup.find_all('tr')
    
    # parse data
    # date: 0, time: 1, temperature: 3, rainfall prob.: 8
    soupDate = threeHour[0].find_all('td', limit=3)[1:] + sevenDay[0].find_all('td')[3:]
    soupTime = threeHour[1].find_all('td')[1:] + sevenDay[1].find_all('td')[5:]
    soupTemp = threeHour[3].find_all('td')[1:]
    soupRain = threeHour[8].find_all('td')[1:] + sevenDay[2].find_all('img')[4:]


    # parse data
    # date: 0, time: 1, temperature: 3 and 4, condition: 2
    #soupDate = sevenDay[0].find_all('td')[3:]
    #soupTime = sevenDay[1].find_all('td')[5:]
    soupHighTemp = sevenDay[3].find_all('td')[5:]
    soupLowTemp = sevenDay[4].find_all('td')[5:]
    #soupCondition = sevenDay[2].find_all('img')[4:]

    # collect data
    # duplicate rainfall probability
    tmpRain = []
    for r in soupRain:
        if r.get('colspan'):
            tmpRain.exten([r.get_text(), r.get_text()])
        else:
            tmpRain.append(r.get_text())
    # concatenate temp
    tmpTemp = [temp.get_text() for temp in soupTemp]
    for i

    res = []
    start = 0
    for day in soupDate:
        start = 0
        checkColspan = lambda col: int(col) if col else 1
        res.append({'numCol': checkColspan(day['colspan']), 
                    'date': day.get_text(),
                    'time': [],
                    'temp': [],
                    'condition': []})
        for index in range(start, start+res[-1]['numCol']):
            res[-1]['time'].append(soupTime[index].get_text())
            res[-1]['temp'].append(soupTemp[index].get_text())
            res[-1]['condition'].append(tmpRain[index])
        start += res[-1]['numCol']



    # get 7 day result
    rawData = (urlopen('http://www.cwb.gov.tw/V7/forecast/town368/7Day/{countyCode}.htm'.
            format(countyCode=countyCode)))
    soup = BeautifulSoup(rawData, 'html.parser')
    divided = soup.find_all('tr')



    # collect data
    start = 0
    for day in soupDate:
        res.append({'numCol': day['colspan'],
                    'date': day.get_text(),
                    'time': [],
                    'temp': [],
                    'condition': []})
        for index in range(start, start+res[-1]['numCol']):
            res[-1]['time'.append(soupTime[index].get_text)]

    for i in range(5):
        res['numCol'].append(int(soupDate[i]['colspan']))
        res['date'].append(soupDate[i].get_text())
    for i in range(10):
        res['time'].append(soupTime[i].get_text())
        res['temp'].append('{L}~{H}'.format(L=soupLowTemp[i].get_text(), 
                                            H=soupHighTemp[i].get_text()))
        res['condition'].append(soupCondition[i]['title'])


    # get AQI
    # http://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa
    rawData = urlopen('http://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa')
    stationID = int(conf[query[0]][query[1]][1])
    aqiData = json.loads(rawData.read().decode('utf8'))['Data']
    #res['aqi'] = aqiData[stationID]['AQI']
    res['aqiStyle'] = aqiData[stationID]['AQIStyle']
    res['site'] = aqiData[stationID]['SiteName']

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

    # typesetting result
    # aqi result
    display = ('{queryDist}\n'
                '空氣品質: \n'
                '    觀測站: {site}\n'
                #'    AQI: {aqi}\n'
                '    空氣品質指標: {quality}\n'
                .format(queryDist=' '.join(query), site=res['site'], quality=res['aqiStyle']))
    # precise prediction
    for i in range(2):
        display += ('{D}\n'
                    '    時間    溫度   降雨機率\n'
                    .format(D='{} {}'.format(res['date'][i][:5], res['date'][i][5:])))
        (for time, temp, rain in res['time'][res['numCol'][i]], 
                                    res['temp'][res['numCol'][i]], 
                                    res['condition'][res['numCol'][i]]):
            display += ('    {TIME}    {TEMP}    {RAIN}\n'
                        .format(TIME=time, TEMP=temp, RAIN=rain))

    for i in range(2, 7):
        display += ('{D}\n'
                    '    時間    溫度    天氣狀況\n'
                    .format(D='{} {}'.format(res['date'][i][:5], res['date'][i][5:])))
        for j in range(sum(res['numCol'][:2]), res['numCol'][i]):
            display += ('    {TIME}    {TEMP}    {COND}\n'
                        .format(TIME=res['time'][j], TEMP=res['temp'][j], COND=res['condition'][j]))

    '''
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
    '''
    return display


if __name__ == '__main__':
    #import pprint
    query = ['台中', '豐原市']
    #pp = pprint.PrettyPrinter(indent=4)
    #pprint.pprint(getWeather(query))
    print(getWeather(query))
