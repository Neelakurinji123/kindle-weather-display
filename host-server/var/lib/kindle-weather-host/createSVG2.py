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
import re
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import locale
from decimal import Decimal, ROUND_HALF_EVEN
import extras.getextraicon as extraicon
import extras.weather_icons as wi
from subprocess import Popen
from OpenWeatherMapAPI import OpenWeatherMap


# Create SVG file
def create_svg(p, t_now, tz, utc, svgfile, pngfile):

    def s_padding(x):
        if x >= 100 : return -5
        elif 100 > x >= 10 : return 10
        elif 10 > x >= 0 : return 30
        elif -10 < x < 0 : return 20
        elif x <= -10 : return 0

    def add_header():
        if p.sunrise_and_sunset == 'True':
            t_sunrise = str(datetime.fromtimestamp(curt_weather[11], tz).strftime("%H:%M"))
            t_sunset = str(datetime.fromtimestamp(curt_weather[12], tz).strftime("%H:%M"))

            # localtime
            maintenant = (str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a, %d %b %H:%M")))
            s = '<text style="text-anchor:start;" font-size="30px" x="20" y="40">{}</text>\n'.format(maintenant)

            s += '<text style="text-anchor:end;" font-size="30px" x="445" y="40">{}</text>\n'.format(t_sunrise)
            s += '<text style="text-anchor:end;" font-size="30px" x="580" y="40">{}</text>\n'.format(t_sunset)
        else:
            maintenant = str.lower(datetime.fromtimestamp(t_now, tz).strftime("%a %Y/%m/%d %H:%M"))

            s = '<text style="text-anchor:start;" font-size="30px" x="20" y="40">{}</text>\n'.format(p.city)
            s += '<text style="text-anchor:end;" font-size="30px" x="580" y="40">{}</text>\n'.format(maintenant)

        return s

    def add_curt_weather():
        # Temperature
        tempEntier = math.floor(curt_weather[5])
        tempDecimale = 10 * (curt_weather[5] - tempEntier)
        s = '<text style="text-anchor:end;" font-size="100px" x="425" y="150">{}</text>\n'.format(int(tempEntier))
        s += '<text style="text-anchor:start;" font-size="50px" x="420" y="145">.{}</text>\n'.format(int(tempDecimale))
        s += '<circle cx="440" cy="80" r="7" stroke="black" stroke-width="3" fill="none"/>\n'
        s += '<text style="text-anchor:start;" font-size="35px" x="450" y="100">{}</text>\n'.format(p.unit['temp'])

        # Humidity
        s += '<text style="text-anchor:end;" font-size="30px" x="400" y="200">{}%</text>\n'.format(round(curt_weather[7]))

        # Pressure
        s += '<text style="text-anchor:end;" font-size="30px" x="550" y="200">'
        s += '{0}{1}</text>\n'.format(round(curt_weather[6]), p.unit['pressure'])

        # Wind
        s += '<text style="text-anchor:end;" font-size="30px" x="550" y="240">'
        s += ' {0} {1}</text>\n'.format(int(curt_weather[8]), p.unit['wind_speed'])
        # description
        s += '<text style="text-anchor:end;" font-size="30px" x="550" y="280">{}</text>\n'.format(curt_weather[3])

        # Max
        s += '<text style="text-anchor:end;" font-size="35px" x="550" y="110">{}</text>\n'.format(int(math.ceil(today_forecast[7])))
        s += '<circle cx="555" cy="90" r="4" stroke="black" stroke-width="3" fill="none"/>\n'
        s += '<text style="text-anchor:start;" font-size="25px" x="560" y="102">{}</text>\n'.format(p.unit['temp'])
        s += '<line x1="490" x2="590" y1="117" y2="117" style="fill:none;stroke:black;stroke-width:1px;"/>\n'

        # Min
        s += '<text style="text-anchor:end;" font-size="35px" x="550" y="150">{}</text>\n'.format(int(math.floor(today_forecast[6])))
        s += '<circle cx="555" cy="130" r="4" stroke="black" stroke-width="3" fill="none"/>\n'
        s += '<text style="text-anchor:start;" font-size="25px" x="560" y="142">{}</text>\n'.format(p.unit['temp'])

        # probability of precipitation
        if (curt_weather[2] == 'Rain' or curt_weather[2] == 'Drizzle' or
                curt_weather[2] == 'Snow' or curt_weather[2] == 'Sleet' or curt_weather[2] == 'Clouds'):

            r = Decimal(curt_weather[14]).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
            s += '<text style="text-anchor:end;" font-size="45px" '
            s += 'x="{0}" y="175">{1:.1f}</text>\n'.format((190 - int(s_padding(r) * 0.64)), r)

        return s


    def add_hourly_forecast():
        # add hourly forecast
        base_x = 60
        base_y = -5
        pos_x = 45
        pos_y = 495
        hourly_icon = list()
        s = str()
        for i in range(3, 12, 3):
            hourly_forecast = p.hourly_forecast(i)
            jour = datetime.fromtimestamp(hourly_forecast[0], tz)

            s += '<text style="text-anchor:end;" font-size="30px" '
            s += 'x="{0}" y="{1}">{2}</text>\n'.format((pos_x + 5), (pos_y - 150), str(i)+'h')

            s += '<text style="text-anchor:end;" font-size="35px" x="{0}" y="{1}">'.format((base_x + pos_x), (base_y + pos_y))
            s += '{}</text>\n'.format(round(hourly_forecast[5]))

            s += '<circle cx="{0}" cy="{1}" r="4" '.format((base_x + pos_x + 5), (base_y + pos_y - 25))
            s += 'stroke="black" stroke-width="2" fill="none"/>\n'

            s += '<text style="text-anchor:start;" font-size="25px" '
            s += 'x="{0}" y="{1}">{2}</text>\n'.format((base_x + pos_x + 10), (base_y + pos_y - 10), p.unit['temp'])

            w = hourly_forecast[2]
            if w == 'Rain' or w == 'Drizzle' or w == 'Snow' or w == 'Sleet' or w == 'Clouds':
                r = Decimal(hourly_forecast[7]).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                s += '<text style="text-anchor:end;" font-size="25px" '
                s += 'x="{0}" y="{1}">{2:.1f}</text>\n'.format(int(pos_x + 67 - s_padding(r) * 0.357), (pos_y - 92), r)

            pos_x += 200

        s += '<line x1="0" x2="600" y1="{0}" y2="{0}" style="fill:none;stroke:black;stroke-width:2px;"/>\n'.format(pos_y + 10)
        s += '<line x1="0" x2="600" y1="{0}" y2="{0}" style="fill:none;stroke:black;stroke-width:2px;"/>\n'.format(pos_y - 185)

        s += '<line x1="200" x2="200" y1="{0}" y2="{1}" style="fill:none;stroke:black;stroke-width:2px;"/>\n'.format((pos_y - 185), (pos_y + 10))
        s += '<line x1="400" x2="400" y1="{0}" y2="{1}" style="fill:none;stroke:black;stroke-width:2px;"/>\n'.format((pos_y - 185), (pos_y + 10))

        return s

    def add_daily_forecast():
        minTemp = math.floor(min([p.daily_forecast(1)[6], p.daily_forecast(2)[6] , p.daily_forecast(3)[6]]))
        maxTemp = math.ceil(max([p.daily_forecast(1)[7], p.daily_forecast(2)[7] , p.daily_forecast(3)[7]]))

        pasTemp = 120 / (maxTemp-minTemp)

        n=575
        daily_icon = list()
        s = str()
        for i in range(1, 4):
            forecast = p.daily_forecast(i)
            tLow = math.floor(forecast[6])
            tHigh = math.ceil(forecast[7])
            jour = datetime.fromtimestamp(forecast[0], tz)
            s += '<text style="text-anchor:end;" font-size="35px" '
            s += 'x="185" y="{0}">{1}</text>\n'.format(n, str.lower(jour.strftime("%A")))

            tMin = (int)(355 + pasTemp * (tLow - minTemp))
            s += '<text style="text-anchor:end;" font-size="35px" '
            s += 'x="{0}" y="{1}">{2}</text>\n'.format(tMin, n, int(tLow))

            s += '<circle cx="{0}" cy="{1}" r="4" stroke="black" stroke-width="2" fill="none"/>\n'.format(tMin+5, (n-25))
            s += '<text style="text-anchor:start;" font-size="25px" x="{0}" y="{1}">{2}</text>\n'.format((tMin+10), (n-10), p.unit['temp'])

            tMax = (int)(440 + pasTemp * (tHigh - minTemp))
            s += '<text style="text-anchor:end;" font-size="35px" '
            s += 'x="{0}" y="{1}">{2}</text>\n'.format(int(tMax - s_padding(tHigh)), n, int(tHigh))

            s += '<circle cx="{0}" cy="{1}" r="4" '.format(int(tMax + 5 - s_padding(tHigh)), (n-25))
            s += 'stroke="black" stroke-width="2" fill="none"/>\n'

            s += '<text style="text-anchor:start;" font-size="25px" '
            s += 'x="{0}" y="{1}">{2}</text>\n'.format(int(tMax + 10 - s_padding(tHigh)), (n-10), p.unit['temp'])

            s += '<line x1="{0}" x2="{1}" y1="{2}" y2="{3}" '.format(int(tMin + 40), int(tMax - 65), (n-10), (n-10))
            s += 'style="fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;"/>\n'

            n += 90

        return s

    def add_sunrise_and_sunset_icons():
        s = '<g transform="matrix(1.1,0,0,1.1,332,14)">{}</g>\n'.format(wi.getSunrise())
        s += '<g transform="matrix(1.1,0,0,1.1,467,14)">{}</g>\n'.format(wi.getSunset())

        return s

    def add_today_icon():
        s = '<g transform="matrix(4,0,0,4,-35,-40)">{}</g>\n'.format(p.current_weather.icon)

        # add wind direction icon
        if int(curt_weather[8]) != 0:
            w = p.cardinal(curt_weather[9])
            if w == 'N':    r = wi.getDirectionDown()
            elif w == 'NE': r = wi.getDirectionDownLeft()
            elif w == 'E':  r = wi.getDirectionLeft()
            elif w == 'SE': r = wi.getDirectionUpLeft()
            elif w == 'S':  r = wi.getDirectionUp()
            elif w == 'SW': r = wi.getDirectionUpRight()
            elif w == 'W':  r = wi.getDirectionRight()
            elif w == 'NW': r = wi.getDirectionDownRight()

            s += '<g transform="matrix(1.6,0,0,1.6,{0},206)">{1}</g>\n'.format((440 - len(str(int(curt_weather[8]))) * 17), r)

        return s

    def add_next_hours_icons():
        n = 8
        s = str()
        for i in range(3, 12, 3):
#            s += '<g transform="matrix(2.3,0,0,2.3,{0},290)">{1}</g>\n'.format((n-25), p.hourly_forecast.icon[i])
            s += '<g transform="matrix(2.3,0,0,2.3,{0},280)">{1}</g>\n'.format((n-25), p.hourly_forecast.icon[i])
            n += 200

        return s

    def add_next_days_icons():
        n = 470
        s = str()
        for i in range(1, 4):
            s += '<g transform="matrix(1.9,0,0,1.9,160,{0})">{1}</g>\n'.format(n, p.daily_forecast.icon[i])
            n += 90

        return s

    today_forecast = p.daily_forecast(0)
    curt_weather = p.current_weather()
    alerts = p.weather_alerts()

    f_svg = open(svgfile,"w", encoding=p.encoding)

    f_svg.write('<?xml version="1.0" encoding="{}"?>\n'.format(p.encoding))
    f_svg.write('<svg xmlns="http://www.w3.org/2000/svg" height="800" width="600" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
    #f_svg.write('<g font-family="Chalkboard">\n')
    #f_svg.write('<g font-family="Arial">\n')
    f_svg.write('<g font-family="{}">\n'.format(p.font))
    f_svg.write(add_header())
    f_svg.write(add_curt_weather())

    if alerts != None:
        pass
    else:
        f_svg.write(add_hourly_forecast())
        f_svg.write(add_daily_forecast())
        f_svg.write('</g>\n')

    if alerts != None:
        n = 425
        s = str()
        s += '<text style="text-anchor:start;" font-weight="bold" font-size="30px" x="20" y="380">'
        s += 'ALERT: {}</text>\n'.format(alerts[0]['event'])
        for r in re.split("\n", alerts[0]['description']):
            s += '<text style="text-anchor:start;" font-size="16px" x="20" y="{0}">{1}</text>\n'.format(n, r)
            n += 30

        f_svg.write(s)
        f_svg.write('</g>\n')
    else:
        if p.sunrise_and_sunset == 'True':
            f_svg.write(add_sunrise_and_sunset_icons())

        f_svg.write(add_next_hours_icons())
        f_svg.write(add_next_days_icons())

    f_svg.write(add_today_icon())

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

