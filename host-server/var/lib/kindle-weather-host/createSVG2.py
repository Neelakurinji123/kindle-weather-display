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
from decimal import Decimal, ROUND_HALF_EVEN
import extras.getextraicon as extraicon
from subprocess import Popen
from OpenWeatherMapAPI import OpenWeatherMap


# Create SVG file
def create_svg(p, t_now, tz, utc, svgfile, pngfile):

    today_forecast = p.forecast_daily(0)
    curt_weather = p.current_weather()

    def add_header():
        if p.sunrise_and_sunset == 'True':
            t_sunrise = str(datetime.fromtimestamp(curt_weather[11], tz).strftime("%H:%M"))
            t_sunset = str(datetime.fromtimestamp(curt_weather[12], tz).strftime("%H:%M"))

            # localtime
            maintenant = (str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a, %d %b %H:%M")))
            s = '<text style="text-anchor:start;" font-size="30px" x="20" y="40">' + maintenant + '</text>\n'

            if ("getSunrise" in dir(extraicon.wi)) == True and ("getSunset" in dir(extraicon.wi)) == True:
                # text
                s += '<text style="text-anchor:end;" font-size="30px" x="445" y="' + str(40) + '">' + t_sunrise + '</text>\n'
                s += '<text style="text-anchor:end;" font-size="30px" x="580" y="' + str(40) + '">' + t_sunset + '</text>\n'

                # icon
                s += '<g transform="matrix(1.1,0,0,1.1,332,' + str(14) + ')">' + extraicon.wi.getSunrise() + '</g>\n'
                s += '<g transform="matrix(1.1,0,0,1.1,467,' + str(14) + ')">' + extraicon.wi.getSunset() + '</g>\n'
            else:
                s += '<text style="text-anchor:end;" font-size="30px" x="580" y="' + str(40) + '">'
                s += 'daytime: ' + t_sunrise + ' - ' + t_sunset + '</text>\n'
        else:
            maintenant = str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a %Y/%m/%d %H:%M"))

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
    if not "wi" in dir(extraicon): (f_svg.write(p.wind_direction(curt_weather[9]) if int(curt_weather[8]) != 0 else ' '))
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
    f_svg.write('<circle cx="555" cy="90" r="4" stroke="black" stroke-width="3" fill="none"/>')
    f_svg.write('<text style="text-anchor:start;" font-size="25px" x="560" y="102">' + p.unit['temp'] + '</text>')

    f_svg.write('<line x1="490" x2="590" y1="117" y2="117" style="fill:none;stroke:black;stroke-width:1px;"/>')

    # Min
    f_svg.write('<text style="text-anchor:end;" font-size="35px" x="550" y="150">')
    f_svg.write("%i" % (math.floor(today_forecast[6])))
    f_svg.write('</text>\n')
    f_svg.write('<circle cx="555" cy="130" r="4" stroke="black" stroke-width="3" fill="none"/>')
    f_svg.write('<text style="text-anchor:start;" font-size="25px" x="560" y="142">' + p.unit['temp'] + '</text>')

    # probability of precipitation
    if (curt_weather[2] == 'Rain' or curt_weather[2] == 'Drizzle' or
            curt_weather[2] == 'Snow' or curt_weather[2] == 'Sleet' or curt_weather[2] == 'Clouds'):

        s = Decimal(curt_weather[14]).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
        f_svg.write('<text style="text-anchor:end;" font-size="45px" x="' + str(190 - int(s_padding(s) * 0.64)) + '" y="175">')
        f_svg.write("%.1f" % s)
        f_svg.write('</text>\n')

   # add hourly forecast
    n = 70
    pos_y = 495
    hourly_icon = list()
    for i in range(3, 12, 3):
        forecast_hourly = p.forecast_hourly(i)
        jour = datetime.fromtimestamp(forecast_hourly[0], tz)

        f_svg.write('<text style="text-anchor:start;" font-size="30px" x="')
        f_svg.write("%i" % (n - 10))
        f_svg.write('" y="')
        f_svg.write("%i" % (pos_y - 160))
        f_svg.write('">')
        f_svg.write(jour.strftime("%H:%M"))
        f_svg.write('</text>')

        f_svg.write('<text style="text-anchor:end;" font-size="35px" x="')
        f_svg.write("%i" % (n + 45))
        f_svg.write('" y="')
        f_svg.write("%i" % (pos_y))
        f_svg.write('">')
        f_svg.write("%i" % (round(forecast_hourly[5])))
        f_svg.write('</text>\n')
        f_svg.write('<circle cx="')
        f_svg.write("%i" % (n + 5 + 45))
        f_svg.write('" cy="')
        f_svg.write("%i" % (pos_y - 25))
        f_svg.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
        f_svg.write('<text style="text-anchor:start;" font-size="25px" x="')
        f_svg.write("%i" % (n + 10 + 45))
        f_svg.write('" y="')
        f_svg.write("%i" % (pos_y - 10))
        f_svg.write('">' + p.unit['temp'] + '</text>\n')

        if (forecast_hourly[2] == 'Rain' or forecast_hourly[2] == 'Drizzle' or
                forecast_hourly[2] == 'Snow' or forecast_hourly[2] == 'Sleet' or forecast_hourly[2] == 'Clouds'):

            s = Decimal(forecast_hourly[7]).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
            f_svg.write('<text style="text-anchor:end;" font-size="25px" x="')
            f_svg.write("%i" % (n + 42 - int(s_padding(s) * 0.357)))
            f_svg.write('" y="')
            f_svg.write("%i" % (pos_y - 82))
            f_svg.write('">')
            f_svg.write("%.1f" % s)
            f_svg.write('</text>\n')

        n += 200

    f_svg.write('<line x1="200" x2="200" y1="' + str(pos_y - 185) + '" y2="' + str(pos_y) + '" style="fill:none;stroke:black;stroke-width:2px;"/>')
    f_svg.write('<line x1="400" x2="400" y1="' + str(pos_y - 185) + '" y2="' + str(pos_y) + '" style="fill:none;stroke:black;stroke-width:2px;"/>')


    # add daily foredast
    minTemp = math.floor(min([p.forecast_daily(1)[6], p.forecast_daily(2)[6] , p.forecast_daily(3)[6]]))
    maxTemp = math.ceil(max([p.forecast_daily(1)[7], p.forecast_daily(2)[7] , p.forecast_daily(3)[7]]))

    pasTemp = 120 / (maxTemp-minTemp)

    n=575
    daily_icon = list()
    for i in range(1, 4):
        forecast = p.forecast_daily(i)
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
    f_svg.write('<g transform="matrix(4,0,0,4,-35,-40)">')
    f_svg.write(p.current_weather.icon)
    f_svg.write('</g>\n')

    # add Wind direction icon
    if "wi" in dir(extraicon) and int(curt_weather[8]) != 0:

        if p.wind_direction(curt_weather[9]) == 'N':
            s = extraicon.wi.getDirectionUp()
        elif p.wind_direction(curt_weather[9]) == 'NE':
            s = extraicon.wi.getDirectionUpRight()
        elif p.wind_direction(curt_weather[9]) == 'E':
            s = extraicon.wi.getDirectionRight()
        elif p.wind_direction(curt_weather[9]) == 'SE':
            s = extraicon.wi.getDirectionDownRight()
        elif p.wind_direction(curt_weather[9]) == 'S':
            s = extraicon.wi.getDirectionDown()
        elif p.wind_direction(curt_weather[9]) == 'SE':
            s = extraicon.wi.getDirectionLeftDown()
        elif p.wind_direction(curt_weather[9]) == 'E':
            s = extraicon.wi.getDirectionLeft()
        elif p.wind_direction(curt_weather[9]) == 'NE':
            s = extraicon.wi.getDirectionUPLeft()

        f_svg.write('<g transform="matrix(1.6,0,0,1.6,' + str(440 - len(str(int(curt_weather[8]))) * 17) + ',207)">')
        f_svg.write(s)
        f_svg.write('</g>\n')

    # add next hours icons
    n = 8
    for i in range(3, 12, 3):
        f_svg.write('<g transform="matrix(2.3,0,0,2.3,')
        f_svg.write("%i" % (n-25))
        f_svg.write(',290)">')
        f_svg.write(p.forecast_hourly.icon[i])
        f_svg.write('</g>\n')
        n += 200

    # add next days icons
    n = 470
    for i in range(1, 4):
        f_svg.write('<g transform="matrix(1.9,0,0,1.9,160,')
        f_svg.write("%i" % (n))
        f_svg.write(')">')
        f_svg.write(p.forecast_daily.icon[i])
        f_svg.write('</g>\n')
        n += 90

    # close file
    f_svg.write('</svg>')
    f_svg.close()


    def img_convert(svgfile, pngfile, mode):
        if mode ==  'lightmode':
            args = ['convert', '-size', '600x800',  '-background', 'white', '-depth', '8', svgfile, pngfile]
            #args = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', '-resize', '600x800', '-colorspace', 'gray', '-type', 'palette', '-geometry', '600x800',$
            output = Popen(args)
        elif mode == 'darkmode':
            args = ['convert', '-size', '600x800',  '-background', 'white', '-depth', '8', '-negate', svgfile, pngfile]
            #args = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', '-resize', '600x800', '-colorspace', 'gray', '-type', 'palette', '-geometry', '600x800',$
            output = Popen(args)


    # image processing
    def img_processing(dark_mode=p.dark_mode):
        if dark_mode == 'True':
            mode = 'darkmode'
        elif dark_mode == 'Auto':
            if curt_weather[11] > t_now or curt_weather[12] < t_now:
                mode = 'darkmode'
            else:
                mode = 'lightmode'
        else:
            mode = 'lightmode'

        if p.encoding == 'iso-8859-1' or p.encoding == 'iso-8859-5':
            img_convert(svgfile, pngfile, mode)
        else:
            # cloudconvert API
            import cloudconvert
            import json

            with open('cloudconvert.json') as f:
                data = json.load(f)

            cloudconvert.configure(api_key=data['api_key'], sandbox=False)

            # upload
            job = cloudconvert.Job.create(payload={
                'tasks': {
                    'upload-my-file': {
                        'operation': 'import/upload'
                    }
                }
            })

            upload_task_id = job['tasks'][0]['id']

            upload_task = cloudconvert.Task.find(id=upload_task_id)
            res = cloudconvert.Task.upload(file_name=svgfile, task=upload_task)

            res = cloudconvert.Task.find(id=upload_task_id)

            # convert
            job = cloudconvert.Job.create(payload={
                 "tasks": {
                     'convert-my-file': {
                         'operation': 'convert',
                         'input': res['id'],
                         'output_format': 'png',
                         'some_other_option': 'value'
                     },
                     'export-my-file': {
                         'operation': 'export/url',
                         'input': 'convert-my-file'
                     }
                 }
             })

            # download
            exported_url_task_id = job['tasks'][1]['id']
            res = cloudconvert.Task.wait(id=exported_url_task_id) # Wait for job completion
            file = res.get("result").get("files")[0]
            res = cloudconvert.download(filename=file['filename'], url=file['url'])  # download and return filename

            args = ['convert', '-flatten', res,  ('pre-' + res)]
            output = Popen(args)
            time.sleep(3)
            img_convert(('pre-' + res), pngfile, mode)

    img_processing()


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
    t_now = p.t_now
    tz = timezone(p.t_timezone)
    utc = pytz.utc

    # set locale
    locale.setlocale(locale.LC_TIME, p.t_locale)

    create_svg(p=p, t_now=t_now, tz=tz, utc=utc, svgfile=svgfile, pngfile=pngfile)
