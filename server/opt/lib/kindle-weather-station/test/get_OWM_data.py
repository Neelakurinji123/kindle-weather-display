#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import time as t
import json
import requests
import os.path


t_now = int(t.time())
settings = 'settings.json'
output = 'output.json'

with open(settings, 'r') as f:
    service = json.load(f)['station']

    city = service['city']
    t_timezone = service['timezone']
    t_locale = service['locale']
    encoding = service['encoding']
    font = service['font']
    sunrise_and_sunset = bool(eval(service['sunrise_and_sunset']))
    darkmode = service['darkmode']
    api_key = service['api_key']
    lat = service['lat']
    lon = service['lon']
    units = service['units']
    lang = service['lang']
    exclude = service['exclude']  
    alerts = bool(eval(service['alerts']))
#    layout = service['layout']
    ramadhan = bool(eval(service['ramadhan'])) if 'ramadhan' in service else False
    cloudconvert = bool(eval(service['cloudconvert']))
    converter = service['converter']
    graph = bool(eval(service['graph'])) if 'graph' in service else None
    graph_object = service['graph_object'] if 'graph_object' in service else None

    s = str()
    s += 'lat=' + lat + '&lon=' + lon
    s += '&units=' + units if units != '' else ''
    s += '&lang=' + lang if lang != '' else ''
    s += '&exclude=' + exclude if exclude != '' else ''
    s += '&appid=' + api_key

#    url = 'https://api.openweathermap.org/data/3.0/onecall?' + s
    url = 'https://api.openweathermap.org/data/2.5/onecall?' + s

    onecall = requests.get(url).json()

with open(output, 'w', encoding='utf-8') as f:
    json.dump(onecall, f, ensure_ascii=False, indent=4)
