#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Date       : 24 April 2024 


import time as t
import math
import sys
import json
import re
import math
from datetime import datetime, timedelta, date
from pytz import timezone
#import pytz
import locale
import shutil
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
import SVGtools
import os.path
import Icons

# i18n translation
i18nfile = './config/i18n.json'

if os.path.exists('IconExtras.py'):
    import IconExtras as IconExtras
else:
    def IconExtras():
        return ''
        

def s_padding(x):
    if x >= 100 : return -5
    elif 100 > x >= 10 : return 10
    elif 10 > x >= 0 : return 30
    elif -10 < x < 0 : return 20
    elif x <= -10 : return 0

def read_i18n(p, file):
    with open(file, 'r') as f:
        try:
            a = json.load(f)["locale"][p.config['locale']]
        except:
            a = dict()
    return a
    
def split_text(wordwrap, text, max_rows):
    s = list()
    d = dict()
    a = list()
    max_rows -= 1
    rows = 0
    for w in text.split():
        if len(''.join(s)) + len(w)  + len(s) > wordwrap and rows < max_rows:
            d[rows] = s
            rows += 1
            s = [w]
            d[rows] = s
        elif len(''.join(s)) + len(w)  + len(s) + 3 > wordwrap and rows == max_rows:
            s.append('...')
            d[rows] = s
            break
        else:
            s.append(w)
            d[rows] = s
    for n in d.values():
        a += [' '.join(n) + '\n']
    return a

def python_encoding(encoding):
    encoding_list={'us-ascii': 'ascii', 'iso-8859-1': 'latin_1', 'iso8859-1': 'latin_1', 'cp819': 'latin_1', \
                        'iso-8859-2': 'iso8859_2', 'iso-8859-4': 'iso8859_4', 'iso-8859-5': 'iso8859_5', \
                        'iso-8859-6': 'iso8859_6', 'iso-8859-7': 'iso8859_7', 'iso-8859-8': 'iso8859_8', \
                        'iso-8859-9': 'iso8859_9', 'iso-8859-10': 'iso8859_10', 'iso-8859-11': 'iso8859_11', \
                        'iso-8859-13': 'iso8859_13', 'iso-8859-14': 'iso8859_14', 'iso-8859-15': 'iso8859_15', \
                        'iso-8859-16': 'iso8859_16', 'utf8': 'utf_8'}
    return encoding_list[encoding]

class Maintenant:
    def __init__(self, p, x, y, variant=None):
        self.p = p
        self.x = x
        self.y = y
        self.variant = variant

    def text(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        tz = timezone(p.config['timezone'])
        now = p.now
        a = str()
        if p.config['sunrise_and_sunset'] == True:
            if weather['sunrise'] == 0:
                sunrise = "--:--"
            else:
                try:
                    sunrise = str(datetime.fromtimestamp(weather['sunrise'], tz).strftime("%H:%M"))
                except Exception as e:
                    sunrise = "--:--"
            if weather['sunset'] == 0:
                sunset = "--:--"
            else:
                try:
                    sunset = str(datetime.fromtimestamp(weather['sunset'], tz).strftime("%H:%M"))
                except Exception as e:
                    sunset = "--:--"
            # localtime
            maintenant = (str.lower(datetime.fromtimestamp(now, tz).strftime("%a, %d %b %H:%M")))
            w = maintenant.split()
            #d = read_i18n(p, i18nfile)
            #w[0] = d["abbreviated_weekday"][w[0][:-1]] + ',' if not d == dict() else w[0]
            #w[2] = d["abbreviated_month"][w[2]] if not d == dict() else w[2]
            if p.config['landscape'] == True:
                #a += SVGtools.text("start", "30px", (x + 200 + 20), (y + 40), ' '.join(w)).svg()
                a += SVGtools.text("end", "30px", (x + 200 + 445), (y + 40), sunrise).svg()
                a += SVGtools.text("end", "30px", (x + 200 + 580),(y + 40), sunset).svg()                
                a += SVGtools.text("start", "30px", (x + 20), (y + 40), p.config['city']).svg()
                a += SVGtools.text("end", "30px", (x + 520), (y + 40), ' '.join(w)).svg()
            else:
                a += SVGtools.text("start", "30px", (x + 20), (y + 40), ' '.join(w)).svg()
                a += SVGtools.text("end", "30px", (x + 445), (y + 40), sunrise).svg()
                a += SVGtools.text("end", "30px", (x + 580),(y + 40), sunset).svg()
        else:
            maintenant = str.lower(datetime.fromtimestamp(now, tz).strftime("%a %Y/%m/%d %H:%M"))
            w = maintenant.split()
            #d = read_i18n(p, i18nfile)
            #w[0] = d["abbreviated_weekday"][w[0]] if not d == dict() else w[0]
            a += SVGtools.text("start", "30px", (x + 20), (y + 40), p.config['city']).svg()
            a += SVGtools.text("end", "30px", (x + 580), (y + 40), ' '.join(w)).svg()

        return a

    def icon(self):
        p, x, y = self.p, self.x, self.y
        a = str()
        if p.config['sunrise_and_sunset'] == True:
            if p.config['landscape'] == True:
                a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 200 + 328) + "," + str(y + 14) + ")", Icons.Sunrise()).svg() 
                a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 200 + 465) + "," + str(y + 14) + ")", Icons.Sunset()).svg()
            else:
                a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 328) + "," + str(y + 14) + ")", Icons.Sunrise()).svg() 
                a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 465) + "," + str(y + 14) + ")", Icons.Sunset()).svg()
        return a


class CurrentData:
    def precipitation(self):
        p, x, y = self.p, self.x, self.y
        config = p.config
        weather = p.CurrentWeather()
        a = str()        
        sub_main = self.sub_main        
        # 'in_clouds' option
        if not config['in_clouds'] == str():
            #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
            if weather['main'] in ['Cloudy']:
                r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                if r == 0:
                    a += SVGtools.text("end", "45px", (x + 200 - int(s_padding(r) * 0.64)), (y + 135), "").svg()
                    #a += SVGtools.text("end", "45px", (x + 200 - int(s_padding(r) * 0.64)), (y + 135), "n/a").svg()
                else:
                    if p.config['landscape'] == True:
                        if weather['main'] == sub_main:
                            a += SVGtools.text("end", "45px", (x + 195 - int(s_padding(r) * 0.64)), (y + 160), \
                                Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                        else:
                            a += SVGtools.text("end", "40px", (x + 162 - int(s_padding(r) * 0.64)), (y + 120), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                    else:
                        if weather['main'] == sub_main:
                            a += SVGtools.text("end", "45px", (x + 195 - int(s_padding(r) * 0.64)), (y + 135), \
                                Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                        else:
                            a += SVGtools.text("end", "40px", (x + 162 - int(s_padding(r) * 0.64)), (y + 120), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
        return a

    def temperature(self):
        p, x, y, offset, wordwrap = self.p, self.x, self.y, self.offset, self.wordwrap
        weather = p.CurrentWeather()
        daily = p.DailyForecast(0)
        a = str()
        # Temperature
        tempEntier = math.floor(weather['temp'])
        tempDecimale = 10 * (weather['temp'] - tempEntier)
        a += SVGtools.text("end", "100px", (x + 155), (y + 315), int(tempEntier)).svg()
        a += SVGtools.text("start", "50px", (x + 150), (y + 310), "." + str(int(tempDecimale))).svg()
        a += self.add_temp_unit(x=x, y=y, font_size=50)
        # Max temp
        a += SVGtools.text("end", "35px", (x + 280), (y + 275), int(math.ceil(daily['temp_max']))).svg()
        a += self.add_temp_unit(x=x, y=y, font_size=35)
        # Line
        a += SVGtools.line((x + 220), (x + 320), (y + 282), (y + 282), "fill:none;stroke:black;stroke-width:1px;").svg()
        # Min temp
        a += SVGtools.text("end", "35px", (x + 280), (y + 315), int(math.ceil(daily['temp_min']))).svg()
        a += self.add_temp_unit(x=x, y=y+40, font_size=35)
        return a

    def add_temp_unit(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 50:
            a += SVGtools.circle((x + 171), (y + 245), 6, "black", 3, "none").svg()
            a += SVGtools.text("start", "35px", (x + 180), (y  + 265), p.units['temp']).svg()
        elif font_size == 35:
            a += SVGtools.circle((x + 285), (y + 252), 4, "black", 2, "none").svg()
            a += SVGtools.text("start", "25px", (x + 290), (y  + 267), p.units['temp']).svg()
        return a

    def pressure(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        _x = -5 if p.config['api'] == 'TomorrowIo' else 0
        a = SVGtools.text("end", "30px", (x + _x + 235 + self.offset),(y + 370), str(round(weather['pressure']))).svg()
        a+= SVGtools.text("end", "23px", (x + 280 + self.offset),(y + 370), p.units['pressure']).svg()
        return a

    def humidity(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        a = SVGtools.text("end", "30px", (x + 132 + self.offset), (y + 370), str(round(weather['humidity']))).svg()
        a += SVGtools.text("end", "23px", (x + 155 + self.offset), (y + 370), "%").svg()
        return a

    def wind(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        a = SVGtools.text("end", "30px", (x + 42 + self.offset),(y + 370), str(int(weather['wind_speed']))).svg()
        a += SVGtools.text("end", "23px", (x + 85 + self.offset),(y + 370), p.units['wind_speed']).svg()
        return a

    def description(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        wordwrap= self.wordwrap
        a = str()
        if p.config['landscape'] == True:
            #disc = split_text(wordwrap=wordwrap, text=weather['description'], max_rows=1)
            disc = [weather['description']]
        else:
            disc = split_text(wordwrap=wordwrap, text=weather['description'], max_rows=2)
        for w in disc:
            a += SVGtools.text("end", "30px", (x + 280 + self.offset), (y + 410), w).svg()
            y += 35
        return a

    def icon(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()
        sub_main = self.sub_main
        if weather['main'] == sub_main:
            return SVGtools.transform("(4,0,0,4," + str(x - 30) + "," + str(y - 80) + ")", addIcon(weather['main'])).svg()
        else:
            a = str()
            a += SVGtools.transform("(3.5,0,0,3.5," + str(x - 40) + "," + str(y - 70) + ")", addIcon(weather['main'])).svg()
            a += SVGtools.transform("(1.6,0,0,1.6," + str(x + 200) + "," + str(y + 90) + ")", addIcon(sub_main)).svg()
            a += SVGtools.line((x + 200), (x + 260), (y + 200), (y + 110), "fill:none;stroke:black;stroke-width:2px;").svg()
            return a
            
    def wind_icon(self):
        p, x, y = self.p, self.x, self.y
        weather = p.CurrentWeather()   
        _x = x - 10 - len(str(int(weather['wind_speed']))) * 17 + self.offset
        return SVGtools.transform("(1.6,0,0,1.6," + str(_x) + "," + str(y + 336) + ")", addIcon(weather['cardinal'])).svg()

class CurrentWeatherPane(CurrentData):
    def __init__(self, p, x, y, offset, wordwrap, variant=None):
        self.p = p
        self.x = x
        self.y = y
        self.offset = offset
        self.wordwrap = wordwrap
        weather = p.CurrentWeather()
        sunrise = weather['sunrise']
        sunset = weather['sunset']
        now = p.now
        tz = timezone(p.config['timezone'])
        this_month = int(datetime.fromtimestamp(now, tz).strftime("%m"))
        self.variant = variant

        try:            
            a = self.daytime(dt=now, sunrise=sunrise, sunset=sunset)
            if a == True:
                self.state = 'day'
            else:
                self.state = 'night'
        # The other way: Northern hemisphere: From Sep to Feb is night, from March to Aug is day, sorthern hemisphere is the exact opposite.
        except Exception as e:
            print(e)
            if float(p.config['lat']) < 0 and 3 < this_month <= 9:
                self.state = 'night'
            elif float(p.config['lat']) < 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
                self.state = 'day'
            elif float(p.config['lat']) > 0 and 3 < this_month <= 9:
                self.state = 'day'
            elif float(p.config['lat']) > 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
                self.state = 'night'
               
        # Fix icons: ClearDay, ClearNight, Few-clouds-day, Few-clouds-night
        b = dict()       
        for n in range(24):          
            weather = p.HourlyForecast(n)
            prob = 0.98
            prob **= n
            if self.state == 'night':
                if re.search('Day', weather['main']):
                    c = re.sub('Day', 'Night', weather['main'])
                else:
                    c = weather['main']
            else:
                if re.search('Night', weather['main']):
                    c = re.sub('Night', 'Day', weather['main'])
                else:
                    c = weather['main']
                    
            if c not in b:
                b[c] = 0
            b[c] += prob  
        self.sub_main = max(b.items(), key=lambda x: x[1])[0]
        
    def text(self):
        p = self.p
        if p.config['landscape'] == True:
            x, y = 270, -135
            prec = super(CurrentWeatherPane, self).precipitation()
            self.x, self.y = x, y+5
            temp = super(CurrentWeatherPane, self).temperature()
            self.x, self.y = x, y+10
            pres = super(CurrentWeatherPane, self).pressure()
            self.x, self.y = x, y+10
            humi = super(CurrentWeatherPane, self).humidity()
            self.x, self.y = x+195, y+50
            wind = super(CurrentWeatherPane, self).wind()
            self.x, self.y = x, y+50
            disc = super(CurrentWeatherPane, self).description()
        else:
            prec = super(CurrentWeatherPane, self).precipitation()
            temp = super(CurrentWeatherPane, self).temperature() 
            pres = super(CurrentWeatherPane, self).pressure() 
            humi = super(CurrentWeatherPane, self).humidity() 
            wind = super(CurrentWeatherPane, self).wind() 
            disc = super(CurrentWeatherPane, self).description()
        return prec + temp + pres + humi + wind + disc

    def icon(self):
        p = self.p
        weather = p.CurrentWeather()
        if p.config['landscape'] == True:
            self.x, self.y = -5, 65
            a = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0:
                #self.x = 450
                self.x, self.y = 475,  -85
                a += super(CurrentWeatherPane, self).wind_icon()
        else:
            a = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0:
                self.x += 10      
                a += super(CurrentWeatherPane, self).wind_icon() 
        return a
        
    def daytime(self, dt, sunrise, sunset):
        config = self.p.config
        tz = timezone(config['timezone'])
        d = datetime.fromtimestamp(dt, tz)
        yrs, mons, days, hrs, mins, _, _, _, _ = d.timetuple()
        _dt = hrs * 60 + mins
        d = datetime.fromtimestamp(sunrise, tz)
        yrs, mons, days, hrs, mins, _, _, _, _ = d.timetuple()
        _sunrise = hrs * 60 + mins
        d = datetime.fromtimestamp(sunset, tz)
        yrs, mons, days, hrs, mins, _, _, _, _ = d.timetuple()
        _sunset = hrs * 60 + mins
        if _dt > _sunrise and _dt < _sunset:
            return True
        else:
            return False


class HourlyWeatherPane:
    def __init__(self, p, x, y, hour, span, step, pitch, variant=None):
        self.p = p
        self.x = x
        self.y = y
        self.hour = hour
        self.span = span
        self.step = step
        self.pitch = pitch
        self.variant = variant

    def text(self):
        p, x, y = self.p, self.x, self.y
        config = self.p.config
        offset, wordwrap = 0, 0
        hour, span, step, pitch = self.hour, self.span, self.step, self.pitch
        a = str() 
        # 3h forecast
        for i in range(hour, span, step):
            weather = p.HourlyForecast(i)
            if p.config['landscape'] == True:
                hrs = {3: "3 hrs", 6: "6 hrs", 9: "9 hrs"}
                a += SVGtools.text("end", "30px", (x + 200), (y + 170), round(weather['temp'])).svg()
                a += self.add_temp_unit(x=(x + 200), y=(y + 175), font_size=35)
                a += SVGtools.text("start", "30px", (x + 65), (y + 170), hrs[i]).svg()
                # 'in_clouds' option
                if not config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                        if r == 0:
                            a += SVGtools.text("end", "25px", int(x + 160 - s_padding(r) * 0.357), (y + 92), '').svg()
                        else:
                            a += SVGtools.text("end", "25px", int(x + 157 - s_padding(r) * 0.357), (y + 92), r).svg()
            else:
                hrs = {3: "three hours", 6: "six hours", 9: "nine hours"}
                d = read_i18n(p, i18nfile)
                if not d == dict():
                    for k in hrs.keys():
                        hrs[k] = d["hours"][hrs[k]]
                # Hourly weather document area (base_x=370 ,base_y=40)
                a += SVGtools.text("end", "35px", (x + 30), (y + 96), round(weather['temp'])).svg()
                #a += SVGtools.text("start", "25px", (x - 0), (y + 165), hrs[i]).svg()
                a += SVGtools.text("end", "25px", (x + 180), (y + 165), hrs[i]).svg()
                a += self.add_temp_unit(x=(x + 30), y=(y + 96), font_size=35)
                # 'in_clouds' option
                if not config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                        if r == 0:
                            a += SVGtools.text("end", "25px", int(x + 140 - s_padding(r) * 0.357), (y + 92), '').svg()
                        else:
                            a += SVGtools.text("end", "25px", int(x + 137 - s_padding(r) * 0.357), (y + 92), r).svg()
            y += pitch
        return a

    def icon(self):
        p, x, y = self.p, self.x, self.y
        hour, span, step, pitch = self.hour, self.span, self.step, self.pitch
        a = str()
        for i in range(hour, span, step):
            weather = p.HourlyForecast(i)
            if p.config['landscape'] == True:
                a += SVGtools.transform("(2.3,0,0,2.3," + str(x + 28) + "," + str(y - 32) + ")", addIcon(weather['main'])).svg()
                y += pitch
            else:
                a += SVGtools.transform("(2.3,0,0,2.3," + str(x + 8) + "," + str(y - 32) + ")", addIcon(weather['main'])).svg()
                y += pitch
        return a
        
    def add_temp_unit(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, "black", 2, "none").svg()
            a += SVGtools.text("start", "25px", (x + 10), (y  - 8), p.units['temp']).svg()
        return a


class DailyWeatherPane:
    def __init__(self, p, x, y, span, pitch, variant=None):
        self.p = p
        self.x = 0
        self.y = 500
        self.pitch = 90
        self.span = 4

    def text(self):
        p, x, y = self.p, self.x, self.y
        day1 = p.DailyForecast(1)
        day2 = p.DailyForecast(2)
        day3 = p.DailyForecast(3)
        pitch, span, offset, wordwrap = self.pitch, self.span , 0, 0
        tz = timezone(p.config['timezone'])
        a = str()
        minTemp = math.floor(min([day1['temp_min'], day2['temp_min'], day3['temp_min']]))
        maxTemp = math.ceil(max([day1['temp_max'], day2['temp_max'] , day3['temp_max']]))
        pasTemp = 120 / (maxTemp-minTemp)
        d = read_i18n(p, i18nfile)
        # Drawing temp bars
        for i in range(1, span):
            weather = p.DailyForecast(i)
            tLow = math.floor(weather['temp_min'])
            tHigh = math.ceil(weather['temp_max'])
            jour = datetime.fromtimestamp(weather['dt'], tz)
            tMin = (int)(x + 355 + pasTemp * (tLow - minTemp))
            tMax = (int)(x + 440 + pasTemp * (tHigh - minTemp))
            w = str.lower(jour.strftime("%A"))
            #w = d["full_weekday"][w] if not d == dict() else w
            a += SVGtools.text("end", "35px", (x + 200), (y + 75), w).svg()
            a += SVGtools.text("end", "35px", tMin, (y + 75), int(tLow)).svg()
            a += self.add_temp_unit(x=tMin, y=(y + 75), font_size=35)
            a += SVGtools.text("end", "35px", int((tMax - s_padding(tHigh))), (y + 75), int(tHigh)).svg()
            a += self.add_temp_unit(x=int((tMax - s_padding(tHigh))), y=(y + 75), font_size=35)
            style = "fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;"
            a += SVGtools.line(int(tMin + 40), int(tMax - 65), (y + 75 - 10), (y + 75 - 10), style).svg()
            y += pitch
        return a

    def icon(self):
        p, x, y = self.p, self.x, self.y
        pitch, span, offset = self.pitch, self.span, 0
        a = str()
        for i in range(1, span):
            weather = p.DailyForecast(i)
            a += SVGtools.transform("(1.9,0,0,1.9,{},{})".format((x + 165), (y -30)), addIcon(weather['main'])).svg()
            y += pitch
        return a
        
    def add_temp_unit(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, "black", 2, "none").svg()
            a += SVGtools.text("start", "25px", (x + 10), (y  - 8), p.units['temp']).svg()
        return a

class TwitterPane:
    def __init__(self, p, x, y, variant=None):
        self.p = p
        self.x = x
        self.y = y
        self.tw = p.config['twitter']
        self.keywords = self.tw['keywords']
        
    def text(self):
        p, x, y, tw, keywords = self.p, self.x, self.y, self.tw, self.keywords
        _y = int(y)
        encoding = p.config['encoding']
        #now, timezone_offset = p.now, p.timezone_offset
        a = str()
        #"twitter": {"screen_name": "tenkijp", "translate": "True", "translate_target": "en", "expiration": "1h", "alternate": "daily"}
        from twikit import Client
        from deep_translator import GoogleTranslator
        screen_name, caption, translate, translate_target = tw['screen_name'], tw['caption'], tw['translate'], tw['translate_target']
        expiration, alternate, alternate_url = tw['expiration'], tw['alternate'], tw['alternate_url']     
        user, password = p.config['twitter_screen_name'], p.config['twitter_password']
        include_keywords, exclude_keywords = keywords['include'], keywords['exclude']
        client = Client('en-US')
        client.login(auth_info_1=user, password=password)
        client.save_cookies('/tmp/cookies.json')
        client.load_cookies(path='/tmp/cookies.json')
        user = client.get_user_by_screen_name(screen_name)
        tweets = user.get_tweets('Tweets', count=1)
        tweets_to_store = []
        for tweet in tweets:
            tweets_to_store.append({
                'created_at': tweet.created_at,
                'favorite_count': tweet.favorite_count,
                'full_text': tweet.full_text,
            })
        pattern = r'http[s]*\S+'
        urls = re.findall(pattern, tweets_to_store[0]['full_text'])
        full_text = re.sub(pattern, '', tweets_to_store[0]['full_text'])
        if translate == "True":
            _b = GoogleTranslator(source='auto', target='en').translate(full_text)
            # Fix EncodeError
            en = python_encoding(encoding)
            b = _b.encode(en, 'ignore').decode(en)
        else:
            b = full_text
        c = include_keywords.split(',')
        processing = False
        for n in c:
            if n == str():
                processing = True
                break
            elif re.search(n, b, re.IGNORECASE):
                processing = True
                break
            else:
                processing = False
        c = exclude_keywords.split(',')
        for n in c:
            if n == str() and processing == True:
                processing = True
                break
            elif n == str() and processing == False:
                processing = False
                break
            elif re.search(n, b, re.IGNORECASE):
                processing = False
                break
        c = int()
        d = {"Jan": 1, "January": 1, "Feb": 2, "February": 2, "Mar": 3, "March": 3, "Apr": 4, "April": 4,
                "May": 5, "Jun": 6, "June": 6, "Jul": 7, "July": 7, "Aug": 8, "August": 8, "Sep": 9,
                "September": 9, "Oct": 10, "October": 10, "Nov": 11, "November":11, "Dec": 12, "December": 12}
        e = tweets_to_store[0]['created_at'].split()
        f = e[3].split(':')
        t_min, t_hour, t_day, t_month, t_year = int(f[1]), int(f[0]), int(e[2]), int(d[e[1]]), int(e[5])
        epoch = datetime(t_year, t_month, t_day, t_hour, t_min, 0).timestamp() + p.timezone_offset # UTC + timezone_offset
        #print('epoch', epoch, p.now, (p.now - epoch - p.timezone_offset))
        #print('timezone offset', p.timezone_offset)
        if re.match(r'[0-9.]+m', expiration):
            c = re.sub(r'([0-9.]+)m', r'\1',expiration)
            c_time = float(c) * 60
        elif re.match(r'[0-9.]+h', expiration):
            c = re.sub(r'([0-9.]+)h', r'\1',expiration)
            c_time = float(c) * 60 * 60

        if p.now - epoch <= c_time and processing == True:
            processing = True
        elif p.now - epoch > c_time and processing == True:
            processing = False

        if processing == True:
            if p.config['landscape'] == True:
                if not caption == str() and not a == None:
                    a += SVGtools.text("middle", "30px", (x + 95), (_y + 35), caption).svg()
                disc = split_text(wordwrap=50, text=b, max_rows=6)
                for w in disc:
                    a += SVGtools.text("start", "25px", (x + 180), (y + 30), w).svg()
                    y += 32
            else:
                if not caption == str() and not a == None:
                    a += SVGtools.text("middle", "25px", (x + 95), (_y + 55), caption).svg()
                disc = split_text(wordwrap=36, text=b, max_rows=8)
                for w in disc:
                    a += SVGtools.text("start", "20px", (x + 180), (y + 50), w).svg()
                    y += 25
            if len(urls) > 0:
                url = urls[0]
            else:
                url = alternate_url
        else:
            a, url = None, None
    
                 
        return a, url, processing
        
    def draw(self, url):
        import io
        import qrcode
        import qrcode.image.svg
        #from qrcode.image.pure import PyPNGImage
        p, tw = self.p, self.tw
        _y = 25
        multiple = 5       
        # define a method to choose which factory metho to use
        # possible values 'basic' 'fragment' 'path'
        method = "basic"
        if method == 'basic':
            # Simple factory, just a set of rects.
            factory = qrcode.image.svg.SvgImage
        elif method == 'fragment':
            # Fragment factory (also just a set of rects)
            factory = qrcode.image.svg.SvgFragmentImage
        elif method == 'path':
            # Combined path factory, fixes white space that may occur when zooming
            factory = qrcode.image.svg.SvgPathImage
        # Set data to qrcode
        img = qrcode.make(url, image_factory = factory)
        stream = io.BytesIO()
        img.save(stream)
        # Save svg file somewhere
        #img.save("qrcode.svg")
        #img2 = qrcode.make(data, image_factory=PyPNGImage)
        #img2.save("qrcode.png")
        a = stream.getvalue().decode()
        # Strip unnecessary codes
        a = re.sub(r'<\?xml.+\?>\n', '', a)
        a = re.sub(r'''<svg width=[^<]+>''', '', a)
        a = re.sub(r'</svg>$', '', a)
        a = re.sub('([0-9]+)mm', r'\1', a)
        # Transformation
        if p.config['landscape'] == True:
            if not tw['caption'] == str():
                offset_x, offset_y = 8, (390 + _y)
            else:
                offset_x, offset_y = 8, 390
        else:
            if not tw['caption'] == str():
                offset_x, offset_y = 8, (560 + _y)
            else:
                offset_x, offset_y = 8, 560
        def multi_x(match):
            d = int(match.group(1))
            d *= multiple
            d += offset_x
            s = 'x="' + str(d) + '"'
            return s
        def multi_y(match):
            d = int(match.group(1))
            d *= multiple
            d += offset_y
            s = 'y="' + str(d) + '"'
            return s
        def multi_w(match):
            d = int(match.group(1))
            d *= multiple
            s = 'width="' + str(d) + '"'
            return s
        def multi_h(match):
            d = int(match.group(1))
            d *= multiple
            s = 'height="' + str(d) + '"'
            return s
        a = re.sub(r'x="([0-9]+)"', multi_x, a)
        a = re.sub(r'y="([0-9]+)"', multi_y, a)
        a = re.sub(r'width="([0-9]+)"', multi_w, a)
        a = re.sub(r'height="([0-9]+)"', multi_h, a)
        return a    
    

class GraphLabel:
    def __init__(self, p, x, y, s, variant=None):
        self.p = p
        self.x = x
        self.y = y + 90
        self.s = s
        self.label = p.config['graph_labels'][s]
        self.variant = variant

    def text(self):
        #if self.s == "hourly_xlabel":
        if re.match('hourly', self.s):    
            a = GraphLabel.hourly(self)
        #elif self.s == "daily_xlabel":
        elif re.match('daily', self.s):    
            a = GraphLabel.daily(self)
        return a
        
    def hourly(self):
        p, x, y, s, label, variant = self.p, self.x, self.y, self.s, self.label, self.variant
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        start, end, step, basis, font_size = label["start"], label["end"], label["step"], label["basis"], label["font-size"]
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        c = 0
        for n in range(start, end, step):
            weather = p.HourlyForecast(n)
            heure = datetime.fromtimestamp(weather['dt'], tz).strftime('%H')
            #_x = x + 10 + int((w - 22) / (end - start - 1)) * n
            _x = int(sp_x + box_size_x * n + box_size_x * 0.5)
            if c % 3 == 0:
            #if int(heure) % 3 == 0:
                heure = re.sub('^0', '', heure)
                a += SVGtools.text("middle", str(font_size) + "px", _x, (y - 9), str(heure)).svg()
            c += 1
        a += '</g>'
        return a
            
    def daily(self):
        p, x, y, s, label, variant = self.p, self.x, self.y, self.s, self.label, self.variant
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        #stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        start, end, step, basis, font_size = label["start"], label["end"], label["step"], label["basis"], label["font-size"]
        end = 6 if p.config['api'] == 'TomorrowIo' and end == 8 else end
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / (end - start)
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        for n in range(start, end, step):
            weather = p.DailyForecast(n)
            jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
            jour = d["abbreviated_weekday"][jour] if not d == dict() else jour
            _x = int(sp_x + box_size_x * (n - start) + box_size_x * 0.5)
            a += SVGtools.text("middle", str(font_size) + "px", _x, (y - 9), str(jour)).svg()
        a += '</g>'
        return a
        
        
class GraphPane:
    def __init__(self, p, x, y, obj, variant=None):
        self.p = p
        self.x = x
        self.y = y + 90
        self.obj = obj
        self.variant = variant

    def draw(self):
        if self.obj['type'] == "line":
            a = self.line()
        elif self.obj['type'] == "bar":
            a = self.bar()
        elif self.obj['type'] == "rect":
            a = self.rect()
        elif self.obj['type'] == "tile":
            a = self.tile()
        return a

    def line(self):
        p, x, y, obj = self.p, self.x, self.y, self.obj
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        start, end, step, basis, title = obj["start"], obj["end"], obj["step"], obj["basis"], obj["title"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" and end == 8 else end
        sp_x = int((800 - w) / 2) if p.config['landscape'] == True else int((600 - w) / 2)
        box_size_x = w / end
        half = box_size_x * 0.5
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])       
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 5), y=(y - h + 10), width=(w + grid - 5), height=(h - 45), style=style).svg()
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, axis)
        # Graph
        points = str()
        c = 0
        if basis == "hour":
            tMin = min([p.HourlyForecast(n)["temp"] for n in range(start, end, step)])
            tMax = max([p.HourlyForecast(n)["temp"] for n in range(start, end, step)])
            tStep = 45 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            _title = title + ', 24 hours'
            for n in range(0, end, step):
                weather = p.HourlyForecast(n)
                #heure = datetime.fromtimestamp(h_weather['dt'], tz).strftime('%H')
                _x = int(x + box_size_x * n + half - 5)
                _y = y - (weather['temp'] - tMin) * tStep - 45
                points += "{},{} ".format(_x, _y)
                points2 = points + "{},{} {},{}".format(_x, (y - 35), (x + int(half) - 5), (y - 35))
                #if int(heure) % 3 == 0:
                if c % 3 == 0:    
                    a += SVGtools.text("end", "16px", (_x + 14), (_y - 9), "{} {}".format(round(int(weather['temp'])), p.units['temp'])).svg()
                    a += SVGtools.circle((_x), (_y - 20), 2, "black", 1, "none").svg()
                c += 1
        elif basis == "day":
            tMin = min([p.DailyForecast(n)['temp_day'] for n in range(start, end, step)])
            tMax = max([p.DailyForecast(n)['temp_day'] for n in range(start, end, step)])
            #tStep = 45 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            if p.config['landscape'] == True:
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            else:
                tStep = 45 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            _title = '{}, {} days'.format(title, str(end))
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                jour = d["abbreviated_weekday"][jour] if not d == dict() else jour
                if p.config['landscape'] == True:
                    _x = int(box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep - 45
                    points += "{},{} ".format(_x, _y)
                    points2 = points + "{},{} {},{}".format(_x, (y - 35), int(half), (y - 35))
                    a += SVGtools.text("end", "25px", (_x + 14+10), (_y - 9-5), "{} {}".format(int(weather['temp_day']), p.units['temp'])).svg()
                    a += SVGtools.circle((_x - 8+10), (_y - 24-5), 3, "black", 2, "none").svg()
                    a += SVGtools.text("start", "18px", 10, (600 - 5), _title).svg()
                else:
                    _x = int(x + box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep - 45
                    points += "{},{} ".format(_x, _y)
                    points2 = points + "{},{} {},{}".format(_x, (y - 35), (x + int(half)), (y - 35))
                    a += SVGtools.text("end", "16px", (_x + 14), (_y - 9), "{} {}".format(int(weather['temp_day']), p.units['temp'])).svg()
                    a += SVGtools.circle((_x), (_y - 20), 2, "black", 1, "none").svg()
                    a += SVGtools.text("start", "16px", x, (y - h + 26), _title).svg()

        style2 = "fill:{};stroke:{};stroke-width:{}px;stroke-linecap:{};".format(fill, fill, "0", stroke_linecap)
        a += SVGtools.polyline(points2, style2).svg()
        style = "fill:none;stroke:{};stroke-width:{}px;stroke-linecap:{};".format(stroke_color, stroke, stroke_linecap)
        a += SVGtools.polyline(points, style).svg()
        # Text
        #a += SVGtools.text("start", "16px", x, (y - h + 26), _title).svg()
        a += '</g>'
        return a

    def bar(self):
        p = self.p
        x, y = self.x, self.y
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        title = obj["title"]
        start, end, step, basis = obj["start"], obj["end"], obj["step"], obj["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" and end == 8 else end
        sp_x = int((800 - w) / 2) if p.config['landscape'] == True else int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 5), y=(y - h + 10), width=(w + grid - 5), height=(h - 45), style=style).svg()
        if basis == "hour" and title == "rain precipitation":
            # Graph
            th = 10.0 # threshold
            _min = min([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)]), 2)
            #_Step = step_size(_Min=_Min, _Max=_Max)
            _title = title + ', 24h'
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(start, end, step):
                weather = p.HourlyForecast(n)
                vol = weather['rainAccumulation']
                base_y = y - h + 105
                _vol = int((vol **(1/3)) * th)
                _x = x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.line(x1=_x, x2=_x, y1=base_y, y2=(base_y - _vol) , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text("middle", "16px", _x, (_y - 10), "{} mm".format(int(round(vol, 0)))).svg()
                    style2 = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(axis_color, axis_color, stroke_linecap, "1")
                    a += SVGtools.line(_x, _x, _y, (_y - 8), style2).svg()

        elif basis == "day" and title == "rain precipitation":
            # Graph
            th = 5.75 # threshold
            _min = min([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _max = max([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)]), 2)
            #_Step = step_size(_Min=_Min, _Max=_Max)
            _title = '{}, {} days'.format(title, str(end))
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                vol = weather['rainAccumulation']
                #width=25
                base_y = y - h + 105
                _vol = int((vol **(1/3)) * th)
                _x = x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.line(x1=_x, x2=_x, y1=base_y, y2=(base_y - _vol) , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text("middle", "16px", _x, (base_y - _vol - 12), "{} mm".format(int(round(vol, 0)))).svg()
                    style2 = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(axis_color, axis_color, stroke_linecap, "1")
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()

        # Baseline
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, 1)
        a += SVGtools.line(x1=(x - 5), x2=(x + w - 5 - grid), y1=(y - 35), y2=(y - 35), style=style).svg()
        # Text
        a += SVGtools.text("start", "16px", x, (y - h + 26), "{}, total: {} mm".format(_title, int(round(_sum)), 0)).svg()
        a += '</g>'
        return a

    def rect(self):
        p = self.p
        x, y = self.x, self.y
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        stroke, stroke_color, fill, stroke_linecap, width = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"], obj["width"]
        title = obj["title"]
        start, end, step, basis = obj["start"], obj["end"], obj["step"], obj["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" and end == 8 else end
        sp_x = int((800 - w) / 2) if p.config['landscape'] == True else int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 5), y=(y - h + 10), width=(w + grid - 5), height=(h - 45), style=style).svg() 
        if basis == "hour" and title == "snow accumulation":
            # Graph
            th = 10.0 # threshold 
            _min = min([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)]), 2)
            _title = title + ', 24h'
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(start, end, step):
                weather = p.HourlyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - h + 105
                _vol = int(vol **(1/3) * th)
                a += SVGtools.rect(x=_x - int(width / 2), y=(base_y - _vol), width=width , height=_vol , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text("middle", "16px", _x, (base_y - _vol - 12), "{} mm".format(int(round(vol, 0)))).svg()
                    style2 = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(axis_color, axis_color, stroke_linecap, "1")
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()

        elif basis == "day" and title == "snow accumulation":
            # Graph
            th = 5.75 # threshold  
            _min = min([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _max = max([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)]), 2) 
            _title = '{}, {} days'.format(title, str(end))
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(0, end, step):
                weather = p.DailyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - h + 105
                _vol = int(vol **(1/3) * th)
                _x = x + int(box_size_x * n + box_size_x * 0.5 - width * 0.5)
                a += SVGtools.rect(x=_x - int(width / 2), y=(base_y - _vol), width=width , height=_vol , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text("middle", "16px", _x, (base_y - _vol - 12), "{} mm".format(int(round(vol, 0)))).svg()
                    style2 = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(axis_color, axis_color, stroke_linecap, "1")
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()
        # Baseline
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, 1)
        a += SVGtools.line(x1=(x - 5), x2=(x + w - 5 - grid), y1=(y - 35), y2=(y - 35), style=style).svg()
        # Text processing
        a += SVGtools.text("start", "16px", x, (y - h + 26), "{}, total: {} mm".format(_title, int(round(_sum)), 0)).svg()
        a += '</g>'
        return a

    def tile(self):
        p, x, y, obj, variant = self.p, self.x, self.y, self.obj, self.variant
        canvas = p.config['graph_canvas']
        grid = canvas['grid']
        basis, title = obj['basis'], obj['title']
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        kwargs = {  'w': w, 'h': h, 'bgcolor': bgcolor, 'axis': axis,
                    'axis_color': canvas['axis_color'], 'grid': canvas["grid"], 'grid_color': canvas['grid_color'],
                    'grid_ext_upper': canvas['grid_ext_upper'], 'grid_ext_lower': canvas['grid_ext_lower'],
                    'title': obj['title'], 'start': obj['start'], 'end': obj['end'], 'step': obj['step'],
                    'basis': obj['basis'], 'stroke': obj['stroke'],
                    'stroke_color': obj['stroke-color'], 'fill': obj['fill'], 'stroke_linecap': obj['stroke-linecap'],
                    'tz': timezone(p.config['timezone']), 'sp_x': sp_x, 'variant': variant}
        # Start
        a = '<g font-family="{}">\n'.format(p.config['font'])   
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, 0)
        #a += SVGtools.rect(x=(x - 10), y=(y - h + 10), width=(w + 10), height=(h - 45), style=style).svg()
        if p.config['landscape'] == True:
            a += SVGtools.rect(x=0, y=(y - h + 10), width=w, height=(h - 45), style=style).svg()
        else:
            a += SVGtools.rect(x=(x-5), y=(y - h + 10), width=(w + grid - 5), height=(h - 45), style=style).svg()
        def daily_weather(p, x, y, w, h, bgcolor, axis, axis_color, grid, grid_color, grid_ext_upper, grid_ext_lower, \
                            stroke, stroke_color, fill, stroke_linecap, \
                            title, start, end, step, basis, tz, sp_x, variant, **kwargs):
            end = 6 if p.config['api'] == 'TomorrowIo' and end == 8 else end
            icon_sp = 20 if p.config['api'] == 'TomorrowIo' else 0
            box_size_x = (w - (end - start - 1) * grid) / (end - start)
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p, i18nfile)
            i, s = str(), str()
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                #jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                _x = int(sp_x + (box_size_x + grid) * (n - start))
                _y = y - 45
                if p.config['landscape'] == True:
                    i += SVGtools.transform("(1.8,0,0,1.8,{},{})".format((_x + 70 - box_size_x * 0.5 + icon_sp), (_y - 180)), addIcon(weather['main'])).svg()
                    s += SVGtools.text("end", "30px", (_x + half), (_y + 5), "/").svg()
                    s += SVGtools.text("end", "30px", (_x + half - 20), (_y + 5), "{}".format(round(weather['temp_min']))).svg()
                    s += SVGtools.circle((_x + half - 18), (_y - 15), 3, "black", 2, "none").svg()
                    s += SVGtools.text("end", "30px", (_x + half + 45), (_y + 5), "{}".format(round(weather['temp_max']))).svg()
                    s += SVGtools.circle((_x + half + 47), (_y - 15), 3, "black", 2, "none").svg()
                    if n < (end - 1):
                        style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_color, stroke_linecap, grid)
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55 - grid_ext_upper), (_y + 10), style).svg()
                else:
                    i += SVGtools.transform("(1.0,0,0,1.0,{},{})".format((_x + 12 - box_size_x * 0.5 + icon_sp), (_y - 100)), addIcon(weather['main'])).svg()
                    s += SVGtools.text("end", "16px", (_x + half), (_y ), "/").svg()
                    s += SVGtools.text("end", "16px", (_x + half - 8), (_y ), "{}".format(round(weather['temp_min']))).svg()
                    s += SVGtools.circle((_x + half - 6), (_y - 10), 2, "black", 1, "none").svg()
                    s += SVGtools.text("end", "16px", (_x + half + 22), (_y ), "{}".format(round(weather['temp_max']))).svg()
                    s += SVGtools.circle((_x + half + 24), (_y - 10), 2, "black", 1, "none").svg()
                    #if n < (end - 1):
                    style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_color, stroke_linecap, grid)
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55), (_y + 10), style).svg()
            return s,i

        def moon_phase(p, x, y, w, h, bgcolor, axis, axis_color, grid, grid_color, stroke, stroke_color, fill, stroke_linecap, \
                             grid_ext_upper, grid_ext_lower, title, start, end, step, basis, tz, sp_x, variant, **kwargs):
            from hijridate import Hijri, Gregorian   
            end = 6 if p.config['api'] == 'TomorrowIo' and end == 8 else end
            box_size_x = (w - (end -1) * grid) / end
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p, i18nfile)
            ramadhan = p.config['ramadhan']
            i, s = str(),str()
            
            def calc_moonphase(day, mon, yrs, half, x, y, r, lat, ramadhan, **kwargsPlus):

                def phase(rad):
                    if (2 * pi / 60) > rad >= 0 or (2 * pi / 60) > (pi * 2 - rad) >= 0:
                        a = 'n'
                    elif (2 * pi / 60) > abs(rad - pi * 0.5) >= 0:
                        a = '1'
                    elif (2 * pi / 60) > abs(rad - pi) >= 0:
                        a = 'f'
                    elif (2 * pi / 60) > abs(rad - pi * 1.5) >= 0:
                        a = '3'
                    else:
                        a = str()
                    return a

                def moonphase(day, mon, yrs):
                    g = Gregorian(yrs, mon, day).to_hijri()
                    _, _, d = g.datetuple()
                    mooncycle = 29.55
                    a = d / mooncycle
                    return a

                def calc_ramadhan(day, mon, yrs):
                    g = Gregorian(yrs, mon, day).to_hijri()
                    if g.month_name() == "Ramadhan":
                        a = "r"
                    else:
                        a = str()
                    return a

                # moon phase:  360d = 2pi(rad)
                #lat = -1  # test
                pi = math.pi
                #rad = weather['moon_phase'] * pi * 2  
                # One call API: 0 or 1:new moon, 0.25:first qurater moon, 0.5:full moon, 0.75:third quarter moon 
                m = moonphase(day, mon, yrs)
                rad = m * pi * 2 if m <= 1 else pi * 2  # hijridate module
                c = 0.025
                m = rad * c * math.cos(rad)
                #rx = _x - 3
                rx = x + half
                ry = y - 53
                rp = r + 2
                #rp = r - 2 # test
                ra1 = 1 * rp
                ra2 = (math.cos(rad) * rp)
                ra3 = 1 * rp
                if lat >= 0:
                    if phase(rad) == "n":
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m ) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                else:
                    if phase(rad) == "n":
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp +ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yrs) if ramadhan == True else str()
                return dm, ps, ram

                      
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                day = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%-d'))
                mon = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%-m'))
                yrs = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%Y'))
                lat = float(p.config['lat'])
                moonrise = "--:--" if weather['moonrise'] == 0 else str(datetime.fromtimestamp(weather['moonrise'], tz).strftime("%H:%M"))
                moonset = "--:--" if weather['moonset'] == 0 else str(datetime.fromtimestamp(weather['moonset'], tz).strftime("%H:%M"))                
                if p.config['landscape'] == True:
                    _x = int(sp_x + (box_size_x + grid) * n) 
                    _y = y - 45

                    # grid
                    if n < (end - 1):
                        style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_color, stroke_linecap, grid)
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55 - grid_ext_upper), (_y + 10), style).svg()                 
                    # Moon icon
                    _y = y - 80
                    r = 30
                    kwargsPlus = {'day': day, 'mon': mon, 'yrs': yrs, 'lat': lat, 'x': _x, 'y': _y, 'r': r, 'half': half, 'ramadhan': ramadhan}
                    dm, ps, ram = calc_moonphase(**kwargsPlus)
                    style = "fill:{};stroke:{};stroke-width:{}px;".format(fill, stroke_color, 1)
                    i += SVGtools.circle((_x + half), (_y - 53), (r + 2), stroke_color, stroke, "none").svg()
                    i += SVGtools.path(dm, style).svg() if ps != 'f' else ''
                    # Text: moonrise and moonset
                    s += SVGtools.text("middle", "25px", (_x + half), (_y + 20), moonrise).svg()
                    #s += SVGtools.text("start", "25px", (_x + 15), (_y + 20), 'r').svg()
                    s += SVGtools.text("middle", "25px", (_x + half), (_y + 43), moonset).svg()
                    #s += SVGtools.text("start", "25px", (_x + 15), (_y + 43), 's').svg()
                    #style = "fill:none;stroke:black;stroke-width:1px;"
                    #i += SVGtools.line((_x + half - 25), (_x  + half + 25), (_y - 6+25), (_y - 6+25), style).svg()
                    # Text: moon phase and ramadhan
                    d = {'n': 'new', '1': 'first', 'f': 'full', '3': 'last'}
                    ps = d[ps] if ps in d else ps
                    ram = 'ram' if ram == 'r' else ram
                    s += SVGtools.text("start", "25px", (_x + 5), (_y - 90), "{}".format(ps)).svg()
                    s += SVGtools.text("end", "25px", (_x + box_size_x - 5), (_y - 80), "{}".format(ram)).svg()
                    s += SVGtools.text("start", "18px", 10, (600 - 5), 'moon phase').svg()
                else:
                    _x = int(sp_x + (box_size_x + grid) * n) 
                    _y = y - 45    
                    r = 18 if end == 6 else 14
                    #if n < (end - 1):
                    style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_color, stroke_linecap, grid)
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55), (_y + 10), style).svg()                 
                    # Moon icon
                    kwargsPlus = {'day': day, 'mon': mon, 'yrs': yrs, 'lat': lat, 'x': _x, 'y': _y, 'r': r, 'half': half, 'ramadhan': ramadhan}
                    dm, ps, ram = calc_moonphase(**kwargsPlus)
                    style = "fill:{};stroke:{};stroke-width:{}px;".format(fill, stroke_color, 1)
                    i += SVGtools.circle((_x + box_size_x / 2), (_y - 53), (r + 2), stroke_color, stroke, "none").svg()
                    i += SVGtools.path(dm, style).svg() if ps != 'f' else ''
                    # Text: moonrise and moonset
                    s += SVGtools.text("middle", "16px", (_x + int(box_size_x * 0.5)), (_y - 10), moonrise).svg()
                    s += SVGtools.text("middle", "16px", (_x + int(box_size_x * 0.5)), (_y + 8), moonset).svg()
                    style = "fill:none;stroke:black;stroke-width:1px;"
                    i += SVGtools.line((_x + half - 25), (_x  + half + 25), (_y - 6), (_y - 6), style).svg()
                    # Text: moon phase and ramadhan 
                    s += SVGtools.text("start", "16px", (_x + 3), (_y - 68), "{}".format(ps)).svg()
                    s += SVGtools.text("end", "16px", (_x + box_size_x - 3), (_y - 68), "{}".format(ram)).svg()

            return s,i
        # Graph
        #points = str()
        if basis == "day" and title == "weather":
            s,i = daily_weather(p, x, y, **kwargs)
            a += s + '</g>' + i
        elif basis == "day" and title == "moon phase":
            s,i = moon_phase(p, x, y, **kwargs)
            a += s + '</g>' + i         
        return a


def addIcon(s):
    if s == 'ClearDay':
        if ("ClearDay" in dir(IconExtras)) == True: return IconExtras.ClearDay()
        else: return Icons.ClearDay()
    elif s == 'ClearNight':
        if ("ClearNight" in dir(IconExtras)) == True: return IconExtras.ClearNight()
        else: return Icons.ClearNight()
    elif s == 'Rain':
        if ("Rain" in dir(IconExtras)) == True: return IconExtras.Rain()
        else: return Icons.Rain()
    elif s == 'Drizzle':
        if ("Drizzle" in dir(IconExtras)) == True: return IconExtras.Drizzle()
        else: return Icons.Rain()
    elif s == 'Thunderstorm':
        if ("Thunderstorm" in dir(IconExtras)) == True: return IconExtras.Thunderstorm()
        else: return Icons.Rain()
    elif s == 'Snow':
        if ("Snow" in dir(IconExtras)) == True: return IconExtras.Snow()
        else: return Icons.Snow()
    elif s == 'Sleet':
        if ("Sleet" in dir(IconExtras)) == True: return IconExtras.Sleet()
        else: return Icons.Snow()
    elif s == 'Wind':
        if ("Wind" in dir(IconExtras)) == True: return IconExtras.Wind()
        else: return Icons.Wind()
    elif s == 'Cloudy':
        if ("Cloudy" in dir(IconExtras)) == True: return IconExtras.Cloudy()
        else: return Icons.Cloudy()
    elif s == 'PartlyCloudyDay':
        if ("PartlyCloudyDay" in dir(IconExtras)) == True: return IconExtras.PartlyCloudyDay()
        else: return Icons.PartlyCloudyDay()
    elif s == 'PartlyCloudyNight':
        if ("PartlyCloudyNight" in dir(IconExtras)) == True: return IconExtras.PartlyCloudyNight()
        else: return Icons.PartlyCloudyNight()
    elif s == 'Mist':
        if ("Mist" in dir(IconExtras)) == True: return IconExtras.Mist()
        else: return Icons.Fog()
    elif s == 'Smoke':
        if ("Smoke" in dir(IconExtras)) == True: return IconExtras.Smoke()
        else: return Icons.Fog()
    elif s == 'Haze':
        if ("Haze" in dir(IconExtras)) == True: return IconExtras.Haze()
        else: return Icons.Fog()
    elif s == 'Dust':
        if ("Dust" in dir(IconExtras)) == True: return IconExtras.Dust()
        else: return Icons.Fog()
    elif s == 'Fog':
        if ("Fog" in dir(IconExtras)) == True: return IconExtras.Fog()
        else: return Icons.Fog()
    elif s == 'Sand':
        if ("Sand" in dir(IconExtras)) == True: return IconExtras.Sand()
        else: return Icons.Fog_icon()
    elif s == 'Dust':
        if ("Dust" in dir(IconExtras)) == True: return IconExtras.Dust()
        else: return Icons.Fog()
    elif s == 'Ash':
        if ("Ash" in dir(IconExtras)) == True: return IconExtras.Ash()
        else: return Icons.Fog()
    elif s == 'Squall':
        if ("Squall" in dir(IconExtras)) == True: return IconExtras.Squall()
        else: return Icons.Rain()
    elif s == 'Tornado':
        if ("Tornado" in dir(IconExtras)) == True: return IconExtras.Tornado()
        else: return Icons.Wind()
    elif s == 'Cyclone':
        if ("Cyclone" in dir(IconExtras)) == True: return IconExtras.Cyclone()
        else: return Icons.Wind()
    elif s == 'Snow2':
        if ("gSnow2" in dir(IconExtras)) == True: return IconExtras.Snow2()
        else: return Icons.Snow()
    elif s == 'N':
        return Icons.DirectionDown()
    elif s == 'NE':
        return Icons.DirectionDownLeft()
    elif s == 'E':
        return Icons.DirectionLeft()
    elif s == 'SE':
        return Icons.DirectionUpLeft()
    elif s == 'S':
        return Icons.DirectionUp()
    elif s == 'SW':
        return Icons.DirectionUpRight()
    elif s == 'W':
        return Icons.DirectionRight()
    elif s == 'NW':
        return Icons.DirectionDownRight()
    else:
        return None

