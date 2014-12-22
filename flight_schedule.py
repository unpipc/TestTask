#!/usr/bin/env python
# -*- coding: utf-8 -*-

#REVIEW Общие замечания
#
# 1. Во-первых, работает только отчасти:
#sergey@sergey-VirtualBox:~/akuzyaev/test_task$ ./flight_schedule.py FRA VIE 2014-12-29 2014-12-31
#
#start/end   Stops   FlyDeal  FlyClassic  FlyFlex   flight duration
#06:55/10:05  1  17,101.00   17,716.00   27,811.00   03:10  
#06:55/16:05  1  15,571.00   16,186.00   27,811.00   09:10  
#07:25/14:05  1  25,439.00   26,049.00   28,879.00   06:40  
#08:25/16:05  1  17,101.00   17,716.00   27,811.00   07:40  
#Traceback (most recent call last):
#  File "./flight_schedule.py", line 96, in <module>
#    fly_deal = td_list[2].find_class('lowest').pop().text_content()
#IndexError: pop from empty list
#
# 2. Хотелось бы, конечно, более структурного подхода к программированию. Например, завести пару служебных 
# функций, чтоб не дублировать код, класс Flight для хранения данных о полёте, etc.
#
# 3. Ожидал увидеть работу с xpath-выражениями.


import sys
import requests
import re
import lxml.html as html

if len(sys.argv) < 4 or len(sys.argv) > 5:
    print 'usage: <from IATA code> <to IATA code> <outboundDate yyyy-MM-dd> <returnDate yyyy-MM-dd optional>'
    raise SystemExit(1)

iata_from = sys.argv[1]
#REVIEW. Напрашивается функция для проверки кода IATA, например is_iata().
if not re.match('^[A-Z]{3}$', iata_from):
    print 'first arg must contain IATA code (3 capital letter)'
    raise SystemExit(1)

iata_to = sys.argv[2]
if not re.match('^[A-Z]{3}$', iata_to):
    print 'second arg must contain IATA code (3 capital letter)'
    raise SystemExit(1)

outbound_date = sys.argv[3]
if not re.match('^20[0-9]{2}-[0-9]{2}-[0-9]{2}$', outbound_date):
    print 'third arg must contain date in yyyy-MM-dd format'
    raise SystemExit(1)

return_date = sys.argv[4] if len(sys.argv) == 5 else ''
if len(return_date) > 0 and not re.match('^20[0-9]{2}-[0-9]{2}-[0-9]{2}$', return_date):
    print 'fourth arg must contain date in yyyy-MM-dd format'
    raise SystemExit(1)

one_way = '0' if len(return_date) > 0 else '1'

session = requests.Session()

#Запрос на получение названий аэропортов
response = session.get('http://www.flyniki.com/en-RU/site/json/suggestAirport.php?searchfor=departures&searchflightid=0'
                       '&departures%5B%5D=&destinations%5B%5D=&suggestsource%5B0%5D=activeairports'
                       '&withcountries=1&withoutroutings=1&promotion%5Bid%5D=&promotion%5Btype%5D='
                       '&routesource%5B0%5D=&routesource%5B1%5D=partner')

response_json = response.json()
from_name = [name[u'name'] for name in response_json[u'suggestList'] if name[u'code'] == iata_from][0]
to_name = [name[u'name'] for name in response_json[u'suggestList'] if name[u'code'] == iata_to][0]

payload = {'departure': iata_from, 'destination': iata_to, 'outboundDate': outbound_date,
           'returnDate': return_date, 'oneway': one_way, 'openDateOverview': '0',
           'adultCount': '1', 'childCount': '0', 'infantCount': '0'}

#Отправляем запрос, получаем id сессии
response = session.get('http://www.flyniki.com/en-RU/booking/flight/vacancy.php', params=payload)


#REVIEW. Нечитаемая конструкция получилась. Лучшее форматирование, возможно, не помешало бы.
ajax_data = u'_ajax%5Btemplates%5D%5B%5D=form&_ajax%5Btemplates%5D%5B%5D=main&_ajax%5B' \
       u'templates%5D%5B%5D=priceoverview&_ajax%5Btemplates%5D%5B%5D=infos&_ajax%5B' \
       u'requestParams%5D%5Bdeparture%5D={0}&_ajax%5BrequestParams%5D%5B' \
       u'destination%5D={1}&_ajax%5BrequestParams%5D%5BreturnDeparture%5D=&_ajax%5B' \
       u'requestParams%5D%5BreturnDestination%5D=&_ajax%5BrequestParams%5D%5BoutboundDate' \
       u'%5D={2}&_ajax%5BrequestParams%5D%5BreturnDate%5D={3}&_ajax%5B' \
       u'requestParams%5D%5BadultCount%5D=1&_ajax%5BrequestParams%5D%5BchildCount%5D=0&' \
       u'_ajax%5BrequestParams%5D%5BinfantCount%5D=0&_ajax%5BrequestParams%5D%5BopenDateO' \
       u'verview%5D=&_ajax%5BrequestParams%5D%5Boneway%5D={4}'.format(from_name, to_name,
                                                                   outbound_date, return_date,
                                                                   '' if one_way == '0' else one_way)

headers = {'Referer': response.url,
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

#Отправляем Post запрос для получения конечных данных
#REVIEW. Можно прямо тут писать session.post(...).json(), раз сам response не нужен.
response = session.post(response.url, data=ajax_data, headers=headers)

#Парсим полученный ответ
response_json = response.json()

html_page = html.document_fromstring(response_json['templates']['main'])

tables = html_page.find_class('outbound block').pop().find_class('flighttable')
#REVIEW. Лучше завести более понятный флаг типа полёта, чем проверка длины строки даты возврата.
if len(return_date) > 0:
    tables.append(html_page.find_class('return block').pop().find_class('flighttable'))

for table in tables:
    #REVIEW. Iterable можно превратить в список конструкцией list(iterable), например, list(table)[1:]
    tbody = [el for el in table][1:]
    if len(tbody) == 0:
        continue

    print '\nstart/end   Stops   FlyDeal  FlyClassic  FlyFlex   flight duration'
    for tr in tbody[0]:
        if tr.attrib['class'] == 'flightdetails':
            print '{0:>8}'.format(tr.getchildren()[0].getchildren()[1].getchildren()[1].text_content()
                                    .replace('\n', '').replace('\t', '').replace('duration of journey: ', ''))
            continue

        td_list = [td for td in tr][1:]
        time = [t for t in td_list[0]]
        fly_deal = td_list[2].find_class('lowest').pop().text_content()
        fly_classic = td_list[3].find_class('lowest').pop().text_content()
        fly_flex = td_list[4].find_class('lowest').pop().text_content()
        print '{0}/{1}{2:>3}{3:>12}{4:>12}{5:>12}'.format(time[0].text, time[1].text,
                td_list[1].text.replace('\n', '').replace('\t', ''),
                fly_deal.replace('\n', '').replace('\t', ''),
                fly_classic.replace('\n', '').replace('\t', ''),
                fly_flex.replace('\n', '').replace('\t', '')),

