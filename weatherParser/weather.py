#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
from .locationCode import country

def getWeather(location, period=None):
    if period:
        rawData = urlopen('http://www.cwb.gov.tw/V7/forecast/town368/7Day/{}.htm'.\
            format(country[location[0].encode('utf8')][location[1].encode('utf8')]))
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
        if numCol[0] != 8:
            numCol.append(int(tmp[2]['colspan']))
            date.append(tmp[2].get_text())
    else:
        numCol.append(1)
        numCol.append(7)
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
    
    # typesetting result
    display = ''.join(location) + '\n'
    if numCol[0] == 8:
        display += ''.join(date) + '\n'
        display += '時間    ' + '溫度   ' + '降雨機率' + '\n'
        for i in range(8):
            display += time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'
    else:
        for j in range(2):
            display += ''.join(date[j]) + '\n'
            display += '時間    ' + '溫度   ' '降雨機率' + '\n'
            for i in range(numCol[j]):
                display += time[i] + '  ' + temp[i] + '     ' + rainprob[i] + '\n'
    return display

if __name__ == '__main__':
    location = ['台北', '內湖']
    print(getWeather(location))
