#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import pprint

output = 'current_formatted.txt'

a = {'dt': 1715605200, 'temp': 16.4, 'feels_like': 16.47, 'pressure': 1012, 'humidity': 91, 'dew_point': 14.93, 'uvi': 0, 'clouds': 100, 'visibility': 10000, 'wind_speed': 4.73, 'wind_deg': 4, 'wind_gust': 8.24, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'pop': 0.36, 'rain': {'1h': 1.78}, 'precipitation': 1.78, 'cardinal': 'N', 'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}

pp = pprint.PrettyPrinter(indent=4)
print(pp.pprint(a))
#print(type(pp.pprint(a)))
#with open(output, 'w', encoding='utf-8') as f:
#    f.write(print(pp.pprint(a)))
