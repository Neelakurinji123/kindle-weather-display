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

import math
import time
import sys
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import locale
from decimal import Decimal, ROUND_HALF_UP
import extras.getextraicon as extraicon
from subprocess import Popen
from OpenWeatherMapAPI import OpenWeatherMap


# Create SVG file
def create_svg(p, t_now, tz, utc, svgfile, pngfile):

    today_forecast = p.forecast_daily(0)
    curt_weather = p.current_weather()
    icon_today = p.icon

    def add_header():
        if p.sunrise_and_sunset == 'True':
            t_sunrise = str(datetime.fromtimestamp(curt_weather[11], tz).strftime("%H:%M"))
            t_sunset = str(datetime.fromtimestamp(curt_weather[12], tz).strftime("%H:%M"))

            # localtime
            maintenant = (str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a, %d %b %H:%M")))
            s = '<text style="text-anchor:start;" font-size="30px" x="20" y="40">' + maintenant + '</text>\n'

            if ("getSunrise" in dir(extraicon)) == True and ("getSunset" in dir(extraicon)) == True:
                # text
                s += '<text style="text-anchor:end;" font-size="30px" x="445" y="' + str(40) + '">' + t_sunrise + '</text>\n'
                s += '<text style="text-anchor:end;" font-size="30px" x="580" y="' + str(40) + '">' + t_sunset + '</text>\n'

                # icon
                s += '<g transform="matrix(0.05,0,0,0.05,335,' + str(15) + ')">' + extraicon.getSunrise() + '</g>\n'
                s += '<g transform="matrix(0.05,0,0,0.05,470,' + str(15) + ')">' + extraicon.getSunset() + '</g>\n'
            else:
                s += '<text style="text-anchor:end;" font-size="30px" x="580" y="' + str(40) + '">'
                s += 'daytime: ' + t_sunrise + ' - ' + t_sunset + '</text>\n'
        else:
            maintenant = (str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a %Y/%m/%d %H:%M")))

            s = '<text style="text-anchor:start;" font-size="30px" x="20" y="40">' + p.city + '</text>\n'
            s += '<text style="text-anchor:end;" font-size="30px" x="580" y="40">' + maintenant + '</text>\n'

        return f_svg.write(s)

    def s_padding(x):
        if x >= 100 : return -5
        elif 100 > x >= 10 : return 10
        elif 10 > x >= 0 : return 30
        elif -10 < x < 0 : return 20
        elif x <= -10 : return 0


    f_svg = open(svgfile,"w", encoding=p.encoding)

    f_svg.write('<?xml version="1.0" encoding="' + p.encoding + '"?>\n')
    f_svg.write('<svg xmlns="http://www.w3.org/2000/svg" height="800" width="600" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
    #f_svg.write('<g font-family="Chalkboard">\n')
    #f_svg.write('<g font-family="Arial">\n')
    f_svg.write('<g font-family="' + p.font + '">\n')

    add_header()

    # Temperature
    tempEntier = math.floor(curt_weather[5])
    tempDecimale = 10 * (curt_weather[5] - tempEntier)
    f_svg.write('<text style="text-anchor:end;" font-size="100px" x="425" y="150">')
    f_svg.write("%i" % (tempEntier))
    f_svg.write('</text>\n')
    f_svg.write('<text style="text-anchor:start;" font-size="50px" x="420" y="145">,')
    f_svg.write("%i" % (tempDecimale))
    f_svg.write('</text>\n')
    f_svg.write('<circle cx="440" cy="80" r="7" stroke="black" stroke-width="3" fill="none"/>')
    f_svg.write('<text style="text-anchor:start;" font-size="35px" x="450" y="100">' + p.unit['temp'] + '</text>')

    f_svg.write('<line x1="490" x2="590" y1="118" y2="118" style="fill:none;stroke:black;stroke-width:1px;"/>')

    # Humidity
    f_svg.write('<text style="text-anchor:end;" font-size="30px" x="400" y="200">')
    f_svg.write("%i" % (round(curt_weather[7])))
    f_svg.write('%</text>\n')

    # Pressure
    f_svg.write('<text style="text-anchor:end;" font-size="30px" x="550" y="200">')
    f_svg.write("%i " % (round(curt_weather[6])) + p.unit['pressure'])
    f_svg.write('</text>\n')

    # Wind
    f_svg.write('<text style="text-anchor:end;" font-size="30px" x="550" y="240">')
    f_svg.write(curt_weather[9] if int(curt_weather[8]) != 0 else ' ')
    f_svg.write(' ')
    f_svg.write("%i" % (curt_weather[8]))
    f_svg.write(' ' + p.unit['wind_speed'] + '</text>\n')

    # description
    f_svg.write('<text style="text-anchor:end;" font-size="30px" x="550" y="280">')
    f_svg.write(curt_weather[3])
    f_svg.write('</text>\n')

    # Max
    f_svg.write('<text style="text-anchor:end;" font-size="35px" x="550" y="110">')
    f_svg.write("%i" % (math.ceil(today_forecast[7])))
    f_svg.write('</text>\n')
    f_svg.write('<circle cx="555" cy="88" r="4" stroke="black" stroke-width="3" fill="none"/>')
    f_svg.write('<text style="text-anchor:start;" font-size="25px" x="560" y="100">' + p.unit['temp'] + '</text>')
    f_svg.write('<text style="text-anchor:end;" font-size="35px" x="550" y="150">')

    # Min
    f_svg.write("%i" % (math.floor(today_forecast[6])))
    f_svg.write('</text>\n')
    f_svg.write('<circle cx="555" cy="130" r="4" stroke="black" stroke-width="3" fill="none"/>')
    f_svg.write('<text style="text-anchor:start;" font-size="25px" x="560" y="142">' + p.unit['temp'] + '</text>')

    # probability of precipitation
    if curt_weather[14] > 0 and (curt_weather[2] == 'Rain' or curt_weather[2] == 'Drizzle' or
            curt_weather[2] == 'Thunderstorm' or curt_weather[2] == 'Snow' or curt_weather[2] == 'Sleet' or
            curt_weather[2] == 'Clouds' or curt_weather[2] == 'Squall'):

        s = curt_weather[14] * 100
        #f_svg.write('<text style="text-anchor:end;" font-size="35px" x="' + str(150 + s_padding(s)) + '" y="165">')
        f_svg.write('<text style="text-anchor:end;" font-size="45px" x="' + str(175 - int(s_padding(s) * 0.64)) + '" y="172">')
        f_svg.write("%i" % s)
        f_svg.write('</text>\n')


   # add hourly forecast
    #n = 60
    n = 70
    pos_y = 490
    hourly_icon = list()
    for i in range(3, 12, 3):
        forecast_hourly = p.forecast_hourly(i)
        hourly_icon += [p.icon]
        jour = datetime.fromtimestamp(forecast_hourly[0], tz)
#        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="')
#        #f_svg.write("%i" % (n + 35))
#        f_svg.write("%i" % (n + 75))
#        f_svg.write('" y="')
#        #f_svg.write("%i" % (pos_y - 160))
#        f_svg.write("%i" % (pos_y))
#        f_svg.write('">')
#        f_svg.write(jour.strftime("%H:%M"))
#        f_svg.write('</text>')

        f_svg.write('<text style="text-anchor:start;" font-size="30px" x="')
#        #f_svg.write("%i" % (n + 35))
        f_svg.write("%i" % (n - 55))
        f_svg.write('" y="')
#        #f_svg.write("%i" % (pos_y - 160))
        f_svg.write("%i" % (pos_y))
        f_svg.write('">')
        f_svg.write(jour.strftime("%H:%M"))
        f_svg.write('</text>')

        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="')
        f_svg.write("%i" % (n + 90))
        f_svg.write('" y="')
        f_svg.write("%i" % (pos_y - 0))
        f_svg.write('">')
        f_svg.write("%i" % (round(forecast_hourly[5])))
        f_svg.write('</text>\n')
        f_svg.write('<circle cx="')
        f_svg.write("%i" % (n + 90 + 5))
        f_svg.write('" cy="')
        f_svg.write("%i" % (pos_y - 25 - 0))
        f_svg.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
        f_svg.write('<text style="text-anchor:start;" font-size="25px" x="')
        f_svg.write("%i" % (n + 90 + 10))
        f_svg.write('" y="')
        f_svg.write("%i" % (pos_y - 10 - 0))
        f_svg.write('">' + p.unit['temp'] + '</text>\n')

        if forecast_hourly[7] > 0 and (forecast_hourly[2] == 'Rain' or forecast_hourly[2] == 'Drizzle' or
                forecast_hourly[2] == 'Thunderstorm' or forecast_hourly[2] == 'Snow' or forecast_hourly[2] == 'Sleet' or
                forecast_hourly[2] == 'Clouds' or forecast_hourly[2] == 'Squall'):
            f_svg.write('<text style="text-anchor:end;" font-size="25px" x="')
            s = round(forecast_hourly[7] * 100)
            f_svg.write("%i" % (n + 32 - int(s_padding(s) * 0.357)))
            f_svg.write('" y="')
            f_svg.write("%i" % (pos_y - 88 - 5))
            f_svg.write('">')
            f_svg.write("%i" % (s))
            f_svg.write('</text>\n')

        n += 200

    #f_svg.write('<line x1="200" x2="200" y1="300" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')
    #f_svg.write('<line x1="400" x2="400" y1="300" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')
    f_svg.write('<line x1="200" x2="200" y1="315" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')
    f_svg.write('<line x1="400" x2="400" y1="315" y2="490" style="fill:none;stroke:black;stroke-width:2px;"/>')


    # add daly foredast
    # Find min max for next days
    forecast_daily1 = p.forecast_daily(1)
    forecast_daily2 = p.forecast_daily(2)
    forecast_daily3 = p.forecast_daily(3)

    minTemp = math.floor(min([p.forecast_daily(1)[6], p.forecast_daily(2)[6] , p.forecast_daily(3)[6]]))
    maxTemp = math.ceil(max([p.forecast_daily(1)[7], p.forecast_daily(2)[7] , p.forecast_daily(3)[7]]))

    pasTemp = 120 / (maxTemp-minTemp)

    n=575
    daily_icon = list()
    for i in range(1, 4):
        forecast = p.forecast_daily(i)
        daily_icon += [p.icon]
        jour = datetime.fromtimestamp(forecast[0], tz)
        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="185" y="')
        f_svg.write("%i" % (n))
        f_svg.write('">')
        f_svg.write(str.lower(jour.strftime("%A")))
        f_svg.write('</text>\n')

        tMin = (int)(355 + pasTemp * (math.floor(forecast[6]) - minTemp))
        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="')
        f_svg.write("%i" % (tMin))
        f_svg.write('" y="')
        f_svg.write("%i" % (n))
        f_svg.write('">')
        f_svg.write("%i" % (math.floor(forecast[6])))
        f_svg.write('</text>\n')
        f_svg.write('<circle cx="')
        f_svg.write("%i" % (tMin+5))
        f_svg.write('" cy="')
        f_svg.write("%i" % (n-25))
        f_svg.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
        f_svg.write('<text style="text-anchor:start;" font-size="25px" x="')
        f_svg.write("%i" % (tMin+10))
        f_svg.write('" y="')
        f_svg.write("%i" % (n-10))
        f_svg.write('">' + p.unit['temp'] + '</text>')

        tMax = (int)(440 + pasTemp * (math.ceil(forecast[7]) - minTemp))
        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="')
        f_svg.write("%i" % (tMax - s_padding(forecast[7])))
        f_svg.write('" y="')
        f_svg.write("%i" % (n))
        f_svg.write('">')
        f_svg.write("%i" % (math.ceil(forecast[7])))
        f_svg.write('</text>\n')
        f_svg.write('<circle cx="')
        f_svg.write("%i" % (tMax + 5 - s_padding(forecast[7])))
        f_svg.write('" cy="')
        f_svg.write("%i" % (n-25))
        f_svg.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
        f_svg.write('<text style="text-anchor:start;" font-size="25px" x="')
        f_svg.write("%i" % (tMax + 10 - s_padding(forecast[7])))
        f_svg.write('" y="')
        f_svg.write("%i" % (n-10))
        f_svg.write('">' + p.unit['temp'] + '</text>')

        f_svg.write('<line x1="')
        f_svg.write("%i" % (tMin + 40))
        f_svg.write('" x2="')
        f_svg.write("%i" % (tMax - 65))
        f_svg.write('" y1="')
        f_svg.write("%i" % (n-10))
        f_svg.write('" y2="')
        f_svg.write("%i" % (n-10))
        f_svg.write('" style="fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;"/>\n')

        n += 90

    f_svg.write('</g>\n')

    # add day icon
    # Clear-day, Clear-night, Rain, Snow, Sleet, Wind, Atmosphere, Clouds, Few-clouds-day or Few-clouds-night

    f_svg.write('<g transform="matrix(4,0,0,4,-35,-40)">')
    f_svg.write(icon_today)
    f_svg.write('</g>\n')

    # add next hours icons
    n = 8
    for i in range(0, 3):
        #f_svg.write('<g transform="matrix(1.9,0,0,1.9,')
        #f_svg.write("%i" % (n))
        #f_svg.write(',300)">')
        f_svg.write('<g transform="matrix(2.3,0,0,2.3,')
        f_svg.write("%i" % (n-25))
        f_svg.write(',275)">')
        f_svg.write(hourly_icon[i])
        f_svg.write('</g>\n')
        n += 200

    # add next days icons
    n = 470
    for i in range(0, 3):
        f_svg.write('<g transform="matrix(1.9,0,0,1.9,160,')
        f_svg.write("%i" % (n))
        f_svg.write(')">')
        f_svg.write(daily_icon[i])
        f_svg.write('</g>\n')
        n += 90

    # close file
    f_svg.write('</svg>')
    f_svg.close()


    # image processing
    def displaymode(mode):
        if mode == 'lightmode':
            args = ['convert', '-size', '600x800',  '-background', 'white', '-depth', '8', svgfile, pngfile]
            output = Popen(args)
        elif mode == 'darkmode':
            args = ['convert', '-size', '600x800',  '-background', 'white', '-depth', '8', '-negate', svgfile, pngfile]
            output = Popen(args)


    if p.dark_mode == 'True':
        displaymode('darkmode')
    elif p.dark_mode == 'Auto':
        if curt_weather[11] > t_now or curt_weather[12] < t_now:
            displaymode('darkmode')
        else:
            displaymode('lightmode')
    else:
        displaymode('lightmode')


if __name__ == "__main__":

    # if using custom settings.xml
    if len(sys.argv) > 1:
        params_file = sys.argv[1]
    else:
        params_file = "settings.xml"

    svgfile = "/tmp/www/ieroStation.svg"
    pngfile = "/tmp/www/kindleStation.png"

    p = OpenWeatherMap(params_file)

    # set timezone
    t_now = int(time.time())
    t_timezone = p.t_timezone
    t_locale = p.t_locale
    tz = timezone(t_timezone)
    utc = pytz.utc

    # set locale
    locale.setlocale(locale.LC_TIME, t_locale)

    create_svg(p=p, t_now=t_now, tz=tz, utc=utc, svgfile=svgfile, pngfile=pngfile)

