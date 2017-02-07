# -*- coding: utf8 -*-

from metroCode import station
from bs4 import BeautifulSoup
from urllib import urlopen

def getDuration(location):
    rawData = urlopen('http://web.metro.taipei/c/2stainfo.asp?s1elect={}&action=query&s2elect={}&submit=%C2%A0%E7%A2%BA%E5%AE%9A%C2%A0'.\
        format(station[location[0]], station[location[1]]))
    
    soup = BeautifulSoup(rawData, 'html.parser')
    divided = soup.find_all('div')

    # parse all kind of prices at 4, 5, 6
    prices = []
    for i in divided[4:7]:
        prices.append(i.get_text())

    # parse duration and how to change line at 11, 12
    duration = divided[11].get_text()
    howto = divided[12].get_text()

    display = '{} => {}\n'.format(location[0], location[1])
    display += '票價\n'
    display += '單程票：{}\n'.format(prices[0].encode('utf8'))
    display += '電子票證：{}\n'.format(prices[1].encode('utf8'))
    display += '敬老卡、愛心卡、愛心陪伴卡：{}\n'.format(prices[2].encode('utf8'))
    display += '乘車時間：{}\n'.format(duration.encode('utf8'))
    display += '乘車方式：{}'.format(howto.encode('utf8'))

    return display

if __name__ == '__main__':
    location = ['六張犁', '台北車站']
    print getDuration(location)