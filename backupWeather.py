#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
from locationCode import country

def getWeather(location, period=None):
    if period:
        rawData = urlopen('http://www.cwb.gov.tw/V7/forecast/town368/7Day/{}.htm'.\
            format(country[location[0]][location[1]]))
    else:
        rawData = urlopen('http://www.cwb.gov.tw/V7/forecast/town368/3Hr/{}.htm'.\
            format(country[location[0]][location[1]]))
    
    soup = BeautifulSoup(rawData, 'html.parser')
    divided = soup.find_all('tr')
    
    # parse date at 0
    tmp = divided[0].find_all('td', limit=3)
    numCol = []
    date = []
    date.append(tmp[1].get_text())
    if tmp[1].get('colspan'):
        numCol.append(int(tmp[1]['colspan']))
    else:
        numCol.append(1)
    if numCol[0] != 8:
        numCol.append(int(tmp[2]['colspan']))
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
        

    print location[0], location[1]
    print date[0], date[1]
    print time[0], time[1]
    print temp[0], temp[1]
    print rainprob[0], rainprob[1]
if __name__ == '__main__':
    location = ['台北', '內湖']
    getWeather(location)
