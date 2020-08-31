#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Author : Greg Fabre - http://www.iero.org
# Public domain source code
# Published March 2015
# Update October 2016

# This code creates an SVG image, ready for Kindle 600x800 screen.
# With weather information from Netatmo weather station and 
# forecast from forecast.io.

# Please fill settings.xml file

import json
import math
import time
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import locale
import requests
import geticon
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP


params_file="settings.xml"
filename = "/tmp/www/ieroStation.svg"

# variables
curt_weather = list()
forecast_day = dict()
forecast_hour = list()
day_or_night = str()
temp_24h = {'temp_min': [], 'temp_max': []}

# Create 

# parse params file
tree = ET.parse(params_file)
root = tree.getroot()
for service in root.findall('service'):
    if service.get('name') == 'station' :
        city = service.find('city').text
        t_timezone = service.find('timezone').text
        t_locale = service.find('locale').text
        encoding = service.find('encoding').text
        font = service.find('font').text

    elif service.get('name') == 'openweathermap' :
        api_key = service.find('api_key').text
        lat = service.find('lat').text
        lng = service.find('lng').text
        units = service.find('units').text
        lang = service.find('lang').text
        exclude = service.find('exclude').text

# set timezone
tz = timezone(t_timezone)
utc = pytz.utc

# set locale
locale.setlocale(locale.LC_TIME, t_locale)

# units
if units == 'metric':
    unit_P = 'hPa'
    unit_W = 'm/s'
    unit_T = 'C'
elif units == 'imperial':
    unit_P = 'hPa'
    unit_W = 'mph'
    unit_T = 'F'
else:
    unit_P = 'hPa'
    unit_W = 'mph'
    unit_T = 'K'

def wind_direction(degree):
    if degree >= 348.75 or degree <= 11.25:
        direction = 'N'
    elif 11.25 < degree < 33.75:
        direction = 'NNE'
    elif 33.75 <= degree <= 56.25:
        direction = 'NE'
    elif 56.25 < degree < 78.75:
        direction = 'ENE'
    elif 78.75 <= degree <= 101.25:
        direction = 'E'
    elif 101.25 < degree < 123.75:
        direction = 'ESE'
    elif 123.75 <= degree <= 146.25:
        direction = 'SE'
    elif 146.25 < degree < 168.75:
        direction = 'SSE'
    elif 168.75 <= degree <= 191.25:
        direction = 'S'
    elif 191.25 < degree < 213.75:
        direction = 'SSW'
    elif 213.75 <= degree <= 236.25:
        direction = 'SW'
    elif 236.25 < degree < 258.75:
        direction = 'WSW'
    elif 258.75 <= degree <= 281.25:
        direction = 'W'
    elif 281.25 < degree < 303.75:
        direction = 'WNW'
    elif 303.75 <= degree <= 326.25:
        direction = 'NW'
    elif 326.25 < degree < 348.75:
        direction = 'NNW'

    return direction

def add_icon(icon):
    if icon  == 'Clear-day' : return svg_file.write(geticon.getClearDay())
    elif icon == 'Clear-night' : return svg_file.write(geticon.getClearNight())
    elif icon == 'Rain' : return svg_file.write(geticon.getRain())
    elif icon == 'Drizzle' : return svg_file.write(geticon.getRain())
    elif icon == 'Thunderstorm' : return svg_file.write(geticon.getThunderstorm())
    elif icon == 'Snow' : return svg_file.write(geticon.getSnow())
    elif icon == 'Sleet' : return svg_file.write(geticon.getSleet())
    elif icon == 'wind' : return svg_file.write(geticon.getWind())
    elif icon == 'Atmosphere' : return svg_file.write(geticon.getFog())
    elif icon == 'Clouds' : return svg_file.write(geticon.getCloudy())
    elif icon == 'Few-clouds-day' : return svg_file.write(geticon.getPartlyCloudyDay())
    elif icon == 'Few-clouds-night' : return svg_file.write(geticon.getPartlyCloudyNight())



# OpenWeathermap API
site1 = 'https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+lng+'&exclude='+exclude+'&units='+units+'&lang='+lang+'&appid='+api_key
curt_data = requests.get(site1).json()

site2 = 'https://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&units='+units+'&lang='+lang+'&appid='+api_key
fc_data = requests.get(site2).json()

# test
#json_open = open('openweathermap-curt.txt', 'r')
#curt_data = json.load(json_open)
#
#json_open = open('openweathermap-forecast.txt', 'r')
#fc_data = json.load(json_open)

# current data
# list: 0:time  1:id  2:weather  3:description  4:icon  5:temp  6:pressure  7:humidity  8:wind_speed  9:wind_deg  10:clouds
#
curt_weather = [curt_data['current']['dt'],
                curt_data['current']['weather'][0]['id'],
                curt_data['current']['weather'][0]['main'],
                curt_data['current']['weather'][0]['description'],
                curt_data['current']['weather'][0]['icon'],
                curt_data['current']['temp'],
                curt_data['current']['pressure'],
                curt_data['current']['humidity'],
                curt_data['current']['wind_speed'],
                wind_direction(curt_data['current']['wind_deg']),
                curt_data['current']['clouds']]

# forecast data
# list: 0:time  1:id  2:weather  3:description  4:icon  5:temp_min  6:temp_max  7:clouds
#
for k in fc_data.keys():
    count = 0
    if k == 'list':
        for data in fc_data[k]:

            # beginning of a day in localtime
            t = datetime.fromtimestamp(data['dt'], tz).astimezone(tz)
            t_utc = datetime(t.year, t.month, t.day, 0, 0, tzinfo=utc)
            t_offset = t_utc.astimezone(tz).utcoffset().days * 60 * 60 * 24 + t_utc.astimezone(tz).utcoffset().seconds
            t_index = int(datetime.timestamp(t_utc)) - int(t_offset)

            if int(t_index) not in forecast_day:
                forecast_day[int(t_index)] = {'temp_min': [], 'temp_max': [], 'clouds': [], 'id': [], 'weather': [], 'description': [], 'icon': []}

            forecast_day[int(t_index)]['temp_min'] += [data['main']['temp_min']]
            forecast_day[int(t_index)]['temp_max'] += [data['main']['temp_max']]
            forecast_day[int(t_index)]['clouds'] += [data['clouds']['all']]
            forecast_day[int(t_index)]['id'] += [data['weather'][0]['id']]
            forecast_day[int(t_index)]['weather'] += [data['weather'][0]['main']]
            forecast_day[int(t_index)]['description'] += [data['weather'][0]['description']]
            forecast_day[int(t_index)]['icon'] += [data['weather'][0]['icon']]

            if count == 0  or count == 1 or count == 2:  # interval 3 hrs
                forecast_hour += [[int(data['dt']), data['weather'][0]['id'], str(data['weather'][0]['main']),
                                     str(data['weather'][0]['description']), str(data['weather'][0]['icon']),
                                     float(data['main']['temp_min']), float(data['main']['temp_max']),
                                     float(data['clouds']['all'])]]

            if count < 8:
                temp_24h['temp_min'] += [float(data['main']['temp_min'])]
                temp_24h['temp_max'] += [float(data['main']['temp_min'])]

            count += 1

# delete today's data
today = int(datetime.fromtimestamp(time.time(), tz).strftime("%d"))
fc_today = int(datetime.fromtimestamp(int(sorted(forecast_day)[0]), tz).strftime("%d"))

if today == fc_today:
    forecast_day.pop(int(sorted(forecast_day)[0]), None)

t = sorted(forecast_day)
forecast = list()
for n in range(0, 4):
    forecast += [[t[n], forecast_day[t[n]]['id'][forecast_day[t[n]]['clouds'].index(max(forecast_day[t[n]]['clouds']))],
                        forecast_day[t[n]]['weather'][forecast_day[t[n]]['clouds'].index(max(forecast_day[t[n]]['clouds']))],
                        forecast_day[t[n]]['description'][forecast_day[t[n]]['clouds'].index(max(forecast_day[t[n]]['clouds']))],
                        forecast_day[t[n]]['icon'][forecast_day[t[n]]['clouds'].index(max(forecast_day[t[n]]['clouds']))],
                        min(forecast_day[t[n]]['temp_min']), max(forecast_day[t[n]]['temp_max']),
                        max(forecast_day[t[n]]['clouds'])]]

# localtime
maintenant = (str.lower(datetime.fromtimestamp(time.time(), tz).strftime("%a")) + ' ' +
                 str(datetime.fromtimestamp(time.time(), tz).strftime("%Y/%m/%d %H:%M")))

# Create SVG file

#svg_file = open(filename,"w")
svg_file = open(filename,"w", encoding=encoding)

svg_file.write('<?xml version="1.0" encoding="' + encoding + '"?>\n')
svg_file.write('<svg xmlns="http://www.w3.org/2000/svg" height="800" width="600" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
#svg_file.write('<g font-family="Chalkboard">\n')
#svg_file.write('<g font-family="Arial">\n')
svg_file.write('<g font-family="' + font + '">\n')

# Parsing values

svg_file.write('<text style="text-anchor:start;" font-size="30px" x="20" y="40">')
svg_file.write(city)
#svg_file.write(', ')
svg_file.write('</text>\n')

svg_file.write('<text style="text-anchor:end;" font-size="30px" x="580" y="40">')
svg_file.write("%s" % (maintenant))
svg_file.write('</text>\n')

# Temperature
tempEntier = math.floor(curt_weather[5])
tempDecimale = 10 * (curt_weather[5] - tempEntier)
svg_file.write('<text style="text-anchor:end;" font-size="100px" x="425" y="150">')
svg_file.write("%i" % (tempEntier))
svg_file.write('</text>\n')
svg_file.write('<text style="text-anchor:start;" font-size="50px" x="420" y="145">,')
svg_file.write("%i" % (tempDecimale))
svg_file.write('</text>\n')
svg_file.write('<circle cx="440" cy="80" r="7" stroke="black" stroke-width="3" fill="none"/>')
svg_file.write('<text style="text-anchor:start;" font-size="35px" x="450" y="100">' + unit_T + '</text>')

svg_file.write('<line x1="490" x2="590" y1="118" y2="118" style="fill:none;stroke:black;stroke-width:1px;"/>')

# Humidity
svg_file.write('<text style="text-anchor:end;" font-size="30px" x="400" y="195">')
svg_file.write("%i" % (round(curt_weather[7])))
svg_file.write('%</text>\n')

# Pressure
svg_file.write('<text style="text-anchor:end;" font-size="30px" x="550" y="195">')
svg_file.write("%i " % (round(curt_weather[6])) + unit_P)
svg_file.write('</text>\n')

# Wind
svg_file.write('<text style="text-anchor:end;" font-size="30px" x="550" y="235">')
svg_file.write(curt_weather[9] if round(curt_weather[8]) != 0 else ' ')
svg_file.write(' ')
svg_file.write("%i" % (curt_weather[8]))
svg_file.write(' ' + unit_W + '</text>\n')

# description
svg_file.write('<text style="text-anchor:end;" font-size="30px" x="550" y="275">')
svg_file.write(curt_weather[3])
svg_file.write('</text>\n')

# Min/Max for today

# Max
svg_file.write('<text style="text-anchor:end;" font-size="35px" x="550" y="110">')
#svg_file.write("%i" % (forecast[0][6]))
svg_file.write("%i" % (math.ceil(max(temp_24h['temp_max']))))
svg_file.write('</text>\n')
svg_file.write('<circle cx="555" cy="88" r="4" stroke="black" stroke-width="3" fill="none"/>')
svg_file.write('<text style="text-anchor:start;" font-size="25px" x="560" y="100">' + unit_T + '</text>')
svg_file.write('<text style="text-anchor:end;" font-size="35px" x="550" y="150">')

# Min
#svg_file.write("%i" % (forecast[0][5]))
svg_file.write("%i" % (math.floor(min(temp_24h['temp_min']))))
svg_file.write('</text>\n')
svg_file.write('<circle cx="555" cy="130" r="4" stroke="black" stroke-width="3" fill="none"/>')
svg_file.write('<text style="text-anchor:start;" font-size="25px" x="560" y="142">' + unit_T + '</text>')

def c_offset(x):
    if x >= 10 : return 10
    elif 10 > x >= 0 : return 30
    elif -10 < x < 0 : return 20
    elif x <= -10 : return 0

# Find min max for next hours

#n = 60
n = 70
pos_y = 490
for i in range(0,3):
    jour = datetime.fromtimestamp(forecast_hour[i][0], tz)
    #svg_file.write('<text style="text-anchor:middle;" font-size="35px" x="')
    #svg_file.write("%i" % (n))
    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
    svg_file.write("%i" % (n + 75))
    svg_file.write('" y="')
    svg_file.write("%i" % (pos_y - 160))
    svg_file.write('">')
    svg_file.write(jour.strftime("%H:%M"))
    svg_file.write('</text>')

    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
    svg_file.write("%i" % (n))
    svg_file.write('" y="')
    svg_file.write("%i" % (pos_y))
    svg_file.write('">')
    svg_file.write("%i" % (math.floor(forecast[i][6])))
    svg_file.write('</text>\n')
    svg_file.write('<circle cx="')
    svg_file.write("%i" % (n + 5))
    svg_file.write('" cy="')
    svg_file.write("%i" % (pos_y - 25))
    svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
    svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
    svg_file.write("%i" % (n + 10))
    svg_file.write('" y="')
    svg_file.write("%i" % (pos_y - 10))
    svg_file.write('">' + unit_T + '</text>')

    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
    svg_file.write("%i" % (n + 80 + 15 - c_offset(forecast[i][5])))
    svg_file.write('" y="')
    svg_file.write("%i" % (pos_y))
    svg_file.write('">')
    svg_file.write("%i" % (math.ceil(forecast[i][5])))
    svg_file.write('</text>\n')
    svg_file.write('<circle cx="')
    svg_file.write("%i" % (n + 95 + 5 - c_offset(forecast[i][5])))
    svg_file.write('" cy="')
    svg_file.write("%i" % (pos_y - 25))
    svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
    svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
    svg_file.write("%i" % (n + 95 + 10 - c_offset(forecast[i][5])))
    svg_file.write('" y="')
    svg_file.write("%i" % (pos_y - 10))
    svg_file.write('">' + unit_T + '</text>')

    svg_file.write('<line x1="')
    svg_file.write("%i" % (n + 42))
    svg_file.write('" x2="')
    svg_file.write("%i" % (n + 28))
    svg_file.write('" y1="')
    svg_file.write("%i" % (460))
    svg_file.write('" y2="')
    svg_file.write("%i" % (490))
    svg_file.write('" style="fill:none;stroke:black;stroke-linecap:round;stroke-width:2px;"/>')

    n += 200

svg_file.write('<line x1="200" x2="200" y1="300" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')
svg_file.write('<line x1="400" x2="400" y1="300" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')

# Find min max for next days
minTemp = math.floor(min([forecast[1][5], forecast[2][5], forecast[3][5]]))
maxTemp = math.ceil(max([forecast[1][6], forecast[2][6], forecast[3][6]]))

#pasTemp = (530-370)/(maxTemp-minTemp)
pasTemp = 90 / (maxTemp-minTemp)

n=575
for i in range(0,3):
    jour = datetime.fromtimestamp(forecast[i][0], tz)
    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="185" y="')
    svg_file.write("%i" % (n))
    svg_file.write('">')
    svg_file.write(str.lower(jour.strftime("%A")))
    svg_file.write('</text>\n')

    tMin = (int)(355 + pasTemp * (math.floor(forecast[i][5]) - minTemp))
    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
    svg_file.write("%i" % (tMin))
    svg_file.write('" y="')
    svg_file.write("%i" % (n))
    svg_file.write('">')
    svg_file.write("%i" % (math.floor(forecast[i][5])))
    svg_file.write('</text>\n')
    svg_file.write('<circle cx="')
    svg_file.write("%i" % (tMin+5))
    svg_file.write('" cy="')
    svg_file.write("%i" % (n-25))
    svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
    svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
    svg_file.write("%i" % (tMin+10))
    svg_file.write('" y="')
    svg_file.write("%i" % (n-10))
    svg_file.write('">' + unit_T + '</text>')

    tMax = (int)(470 + pasTemp * (math.ceil(forecast[i][6]) - minTemp))
    svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
    svg_file.write("%i" % (tMax - c_offset(forecast[i][6])))
    svg_file.write('" y="')
    svg_file.write("%i" % (n))
    svg_file.write('">')
    svg_file.write("%i" % (math.ceil(forecast[i][6])))
    svg_file.write('</text>\n')
    svg_file.write('<circle cx="')
    svg_file.write("%i" % (tMax + 5 - c_offset(forecast[i][6])))
    svg_file.write('" cy="')
    svg_file.write("%i" % (n-25))
    svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
    svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
    svg_file.write("%i" % (tMax + 10 - c_offset(forecast[i][6])))
    svg_file.write('" y="')
    svg_file.write("%i" % (n-10))
    svg_file.write('">' + unit_T + '</text>')

    if (tMax-tMin > 50) :
        svg_file.write('<line x1="')
        svg_file.write("%i" % (tMin + 40))
        svg_file.write('" x2="')
        svg_file.write("%i" % (tMax - 65))
        svg_file.write('" y1="')
        svg_file.write("%i" % (n-10))
        svg_file.write('" y2="')
        svg_file.write("%i" % (n-10))
        svg_file.write('" style="fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;"/>')

    n += 90

svg_file.write('</g>\n')

# add day icon
# Clear-day, Clear-night, Rain, Snow, Sleet, Wind, Atmosphere, Clouds, Few-clouds-day or Few-clouds-night

day_or_night = 'day' if curt_weather[4][-1] == 'd' else 'night'
if curt_weather[2] == 'Clear':
    icon = curt_weather[2] + '-' + day_or_night
elif curt_weather[2] == 'Clouds' and curt_weather[3] == 'few clouds':
    icon = 'Few-clouds' + '-' + day_or_night
else:
    icon = curt_weather[2]

svg_file.write('<g transform="matrix(4,0,0,4,-35,-40)">')
add_icon(icon)
svg_file.write('</g>\n')


# add next hours icons
n = 8
for i in range(0,3) :
    day_or_night = 'day' if forecast_hour[i][4][-1] == 'd' else 'night'
    svg_file.write('<g transform="matrix(1.9,0,0,1.9,')
    svg_file.write("%i" % (n))
    svg_file.write(',300)">')

    if forecast_hour[i][2] == 'Clear':
        icon = forecast_hour[i][2] + '-' + day_or_night
    elif forecast_hour[i][2] == 'Clouds' and forecast_hour[i][3] == 'few clouds':
        icon = 'Few-clouds' + '-' + day_or_night
    else:
        icon = forecast_hour[i][2]

    add_icon(icon)
    n += 200
    svg_file.write('</g>\n')

# add next days icons

n=470
day_or_night = 'day' if curt_weather[4][-1] == 'd' else 'night'
for i in range(1,4) :
    svg_file.write('<g transform="matrix(1.9,0,0,1.9,160,')
    svg_file.write("%i" % (n))
    svg_file.write(')">')

    if forecast[i][2] == 'Clear':
        icon = forecast[i][2] + '-' + day_or_night
    elif forecast[i][2] == 'Clouds' and forecast[i][3] == 'few clouds':
        icon = 'Few-clouds' + '-' + day_or_night
    else:
        icon = forecast[i][2]

    add_icon(icon)
    n += 90
    svg_file.write('</g>\n')

# close file 
svg_file.write('</svg>')
svg_file.close()


