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
    
def split_text(wordwrap, text, max_row):
    s = list()
    d = dict()
    a = list()
    row = 0
    for w in text.split():
        if len(''.join(s)) + len(w)  + len(s) > wordwrap and row < max_row:
            d[row] = s
            row += 1
            s = [w]
            d[row] = s
        elif len(''.join(s)) + len(w)  + len(s) + 3 > wordwrap and row == max_row:
            s.append('...')
            d[row] = s
            break
        else:
            s.append(w)
            d[row] = s
    for n in d.values():
        a += [' '.join(n) + '\n']
    return a

def add_temp_unit(x, y, text, unit):
    a = str()
    a += SVGtools.text("end", "35px", x, y, text).svg()
    a += SVGtools.circle((x + 5), (y - 25), 4, "black", 2, "none").svg()
    a += SVGtools.text("start", "25px", (x + 10), (y  - 10), unit).svg()
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
    def __init__(self, p, x, y):
        self.p = p
        self.x = x
        self.y = y

    def text(self):
        p = self.p
        weather = p.CurrentWeather()
        tz = timezone(p.config['timezone'])
        now = p.now
        x = self.x
        y = self.y
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
        p = self.p
        x = self.x
        y = self.y
        a = str()
        if p.config['sunrise_and_sunset'] == True:
            #a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 332) + "," + str(y + 14) + ")", Icons.Sunrise()).svg() 
            #a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 467) + "," + str(y + 14) + ")", Icons.Sunset()).svg()
            a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 328) + "," + str(y + 14) + ")", Icons.Sunrise()).svg() 
            a += SVGtools.transform("(1.1,0,0,1.1," + str(x + 465) + "," + str(y + 14) + ")", Icons.Sunset()).svg()
        return a


class CurrentData:
    def precipitation(self):
        p = self.p
        config = self.p.config
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        a = str()        
        sub_main = self.sub_main        
        # 'in_clouds' option
        if not config['in_clouds'] == str():
            if (weather['main'] == 'Rain' or weather['main'] == 'Drizzle' or
                    weather['main'] == 'Snow' or weather['main'] == 'Sleet' or weather['main'] == 'Cloudy'):
                r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                if r == 0:
                    a += SVGtools.text("end", "45px", (x + 200 - int(s_padding(r) * 0.64)), (y + 135), "").svg()
                    #a += SVGtools.text("end", "45px", (x + 200 - int(s_padding(r) * 0.64)), (y + 135), "n/a").svg()
                else:
                    if weather['main'] == sub_main:
                        a += SVGtools.text("end", "45px", (x + 195 - int(s_padding(r) * 0.64)), (y + 135), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                    else:
                        a += SVGtools.text("end", "40px", (x + 172 - int(s_padding(r) * 0.64)), (y + 120), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
        return a

    def temperature(self):
        p = self.p
        weather = p.CurrentWeather()
        daily = p.DailyForecast(0)
        x = self.x
        y = self.y
        offset = self.offset
        wordwrap= self.wordwrap
        a = str()
        # Temperature
        tempEntier = math.floor(weather['temp'])
        tempDecimale = 10 * (weather['temp'] - tempEntier)
        a += SVGtools.text("end", "100px", (x + 155), (y + 315), int(tempEntier)).svg()
        a += SVGtools.text("start", "50px", (x + 150), (y + 310), "." + str(int(tempDecimale))).svg()
        a += SVGtools.circle((x + 171), (y + 245), 6, "black", 3, "none").svg()
        a += SVGtools.text("start", "35px", (x + 180), (y + 265), p.units['temp']).svg()
        # Max temp
        a += SVGtools.text("end", "35px", (x + 280), (y + 275), int(math.ceil(daily['temp_max']))).svg()
        a += SVGtools.circle((x + 285), (y + 255), 4, "black", 2, "none").svg()
        a += SVGtools.text("start", "25px", (x + 290), (y + 267), p.units['temp']).svg()
        # Line
        a += SVGtools.line((x + 220), (x + 320), (y + 282), (y + 282), "fill:none;stroke:black;stroke-width:1px;").svg()
        # Min temp
        a += SVGtools.text("end", "35px", (x + 280), (y + 315), int(math.ceil(daily['temp_min']))).svg()
        a += SVGtools.circle((x + 285), (y + 295), 4, "black", 2, "none").svg()
        a += SVGtools.text("start", "25px", (x + 290), (y + 307), p.units['temp']).svg()
        return a

    def pressure(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        a = SVGtools.text("end", "30px", (x + 235 + self.offset),(y + 370), str(round(weather['pressure']))).svg()
        a+= SVGtools.text("end", "23px", (x + 280 + self.offset),(y + 370), p.units['pressure']).svg()
        return a

    def humidity(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        a = SVGtools.text("end", "30px", (x + 132 + self.offset), (y + 370), str(round(weather['humidity']))).svg()
        a += SVGtools.text("end", "23px", (x + 155 + self.offset), (y + 370), "%").svg()
        return a

    def wind(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        a = SVGtools.text("end", "30px", (x + 42 + self.offset),(y + 370), str(int(weather['wind_speed']))).svg()
        a += SVGtools.text("end", "23px", (x + 85 + self.offset),(y + 370), p.units['wind_speed']).svg()
        return a

    def description(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        wordwrap= self.wordwrap
        a = str()
        disc = split_text(wordwrap=wordwrap, text=weather['description'], max_row=3)

        for w in disc:
            a += SVGtools.text("end", "30px", (x + 280 + self.offset), (y + 410), w).svg()
            y += 35
        return a

    def icon(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y
        sub_main = self.sub_main
        if weather['main'] == sub_main:
            return SVGtools.transform("(4,0,0,4," + str(x - 30) + "," + str(y - 80) + ")", addIcon(weather['main'])).svg()
        else:
            a = str()
            a += SVGtools.transform("(3.5,0,0,3.5," + str(x - 30) + "," + str(y - 70) + ")", addIcon(weather['main'])).svg()
            a += SVGtools.transform("(1.6,0,0,1.6," + str(x + 200) + "," + str(y + 90) + ")", addIcon(sub_main)).svg()
            a += SVGtools.line((x + 200), (x + 260), (y + 200), (y + 110), "fill:none;stroke:black;stroke-width:2px;").svg()
            return a
            
    def wind_icon(self):
        p = self.p
        weather = p.CurrentWeather()
        x = self.x
        y = self.y       
        _x = x - 10 - len(str(int(weather['wind_speed']))) * 17 + self.offset
        return SVGtools.transform("(1.6,0,0,1.6," + str(_x) + "," + str(y + 336) + ")", addIcon(weather['cardinal'])).svg()

class CurrentWeatherPane(CurrentData):
    def __init__(self, p, x, y, offset, wordwrap):
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
        offset = 0
        a = str()
        a += super(CurrentWeatherPane, self).icon()
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


class CurrentWeatherPane2(CurrentData):
    def __init__(self, p, x, y, offset, wordwrap):
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
        
    def text(self):
        a = str()
        x, y = 270, -165
        a += super(CurrentWeatherPane2, self).precipitation()
        self.x = x
        self.y = y+5
        a += super(CurrentWeatherPane2, self).temperature()
        self.x = x
        self.y = y
        a += super(CurrentWeatherPane2, self).pressure()
        self.x = x
        self.y = y
        a += super(CurrentWeatherPane2, self).humidity()
        self.x = x+195
        self.y = y+40
        a += super(CurrentWeatherPane2, self).wind()
        self.x = x
        self.y = y+40
        a += super(CurrentWeatherPane2, self).description()
        return a

    def icon(self):
        p = self.p
        a = str()
        weather = p.CurrentWeather()
        self.x = -5
        self.y = 45
        a += super(CurrentWeatherPane2, self).icon()
        if int(weather['wind_speed']) != 0:
            #self.x = 450
            self.x = 475
            self.y = -125
            a += super(CurrentWeatherPane2, self).wind_icon()

        return a


class HourlyWeatherPane:
    def __init__(self, p, x, y, hour, span, step, pitch):
        self.p = p
        self.x = x
        self.y = y
        self.hour = hour
        self.span = span
        self.step = step
        self.pitch = pitch

    # Hourly weather document area (base_x=370 ,base_y=40)
    def text(self):
        p, x, y = self.p, self.x, self.y
        config = self.p.config
        offset, wordwrap = 0, 0
        hour, span, step, pitch = self.hour, self.span, self.step, self.pitch
        a = str() 
        # 3h forecast
        for i in range(hour, span, step):
            weather = p.HourlyForecast(i)
            hrs = {3: "three hours", 6: "six hours", 9: "nine hours"}
            d = read_i18n(p, i18nfile)
            if not d == dict():
                for k in hrs.keys():
                    hrs[k] = d["hours"][hrs[k]]

            #a += SVGtools.text("start", "25px", (x - 0), (y + 165), hrs[i]).svg()
            a += SVGtools.text("end", "25px", (x + 180), (y + 165), hrs[i]).svg()
            a += add_temp_unit(x=(x + 30), y=(y + 96), text=round(weather['temp']), unit=p.units['temp'])

            # 'in_clouds' option
            if not config['in_clouds'] == str():
                if weather['main'] == 'Rain' or weather['main'] == 'Drizzle' or weather['main'] == 'Snow' \
                        or weather['main'] == 'Sleet' or weather['main'] == 'Cloudy':
                    #r = Decimal(h_weather['pop']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                    r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                    if r == 0:
                        a += SVGtools.text("end", "25px", int(x + 140 - s_padding(r) * 0.357), (y + 92), '').svg()
                        #a += SVGtools.text("end", "25px", int(x + 140 - s_padding(r) * 0.357), (y + 92), 'n/a').svg()
                    else:
                        a += SVGtools.text("end", "25px", int(x + 137 - s_padding(r) * 0.357), (y + 92), r).svg()
            y += pitch
        return a

    def icon(self):
        p, x, y = self.p, self.x, self.y
        hour, span, step, pitch  = self.hour, self.span, self.step, self.pitch
        a = str()
        for i in range(hour, span, step):
            weather = p.HourlyForecast(i)
            a += SVGtools.transform("(2.3,0,0,2.3," + str(x + 8) + "," + str(y - 32) + ")", addIcon(weather['main'])).svg()
            y += pitch
        return a


class DailyWeatherPane:
    def __init__(self, p, x, y, span, pitch):
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
            a += add_temp_unit(x=tMin, y=(y + 75), text=int(tLow), unit=p.units['temp'])
            a += add_temp_unit(x=int(tMax - s_padding(tHigh)), y=(y + 75), text=int(tHigh), unit=p.units['temp'])
            a += SVGtools.line(int(tMin + 40), int(tMax - 65), (y + 75 - 10), (y + 75 - 10), \
                 "fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;").svg()
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


class TwitterPane:
    def __init__(self, p, x, y):
        self.p = p
        self.x = x
        self.y = y
        self.tw_config = p.config['twitter']

    def text(self):
        p, x, y = self.p, self.x, self.y
        _y = int(y)
        tw_config = self.tw_config
        encoding = p.config['encoding']
        now = p.now
        timezone_offset = p.timezone_offset
        a = str()
        #"twitter": {"screen_name": "tenkijp", "translate": "True", "translate_target": "en", "expiration": "1h", "alternate": "daily"}
        from twikit import Client
        from deep_translator import GoogleTranslator
            
        screen_name = tw_config['screen_name']
        translate = tw_config['translate']
        translate_target = tw_config['translate_target']
        expiration = tw_config['expiration']
        alternate = tw_config['alternate']
        user = p.config['twitter_screen_name']
        password = p.config['twitter_password']
        caption = p.config['twitter']['caption']
        alternate_url = tw_config['alternate_url']
        include_keywords = p.config['twitter_include_keywords']
        exclude_keywords = p.config['twitter_exclude_keywords']
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
        epoch = datetime(t_year, t_month, t_day, t_hour, t_min, 0).timestamp() + timezone_offset # UTC + timezone_offset
        #print('epoch', epoch, now, (now - epoch - timezone_offset))
        #print('timezone offset', p.timezone_offset)
        if re.match(r'[0-9.]+m', expiration):
            c = re.sub(r'([0-9.]+)m', r'\1',expiration)
            c_time = float(c) * 60
        elif re.match(r'[0-9.]+h', expiration):
            c = re.sub(r'([0-9.]+)h', r'\1',expiration)
            c_time = float(c) * 60 * 60

        if now - epoch <= c_time and processing == True:
            processing = True
        elif now - epoch > c_time and processing == True:
            processing = False

        if processing == True:
            disc = split_text(wordwrap=36, text=b, max_row=8)
            for w in disc:
                a += SVGtools.text("start", "20px", (x + 180), (y + 50), w).svg()
                y += 25
            if len(urls) > 0:
                url = urls[0]
            else:
                url = alternate_url
        else:
            a, url = None, None
    
        if not tw_config['caption'] == str() and not a == None:
            a += SVGtools.text("middle", "25px", (x + 95), (_y + 55), tw_config['caption']).svg()           
        return a, url, processing
        
    def draw(self, url):
        import io
        import qrcode
        import qrcode.image.svg
        #from qrcode.image.pure import PyPNGImage

        tw_config = self.tw_config
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
        if not tw_config['caption'] == str():
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
    def __init__(self, p, x, y, s):
        self.p = p
        self.x = x
        self.y = y + 90
        self.s = s
        self.label = p.config['graph_labels'][s]

    def text(self):
        #if self.s == "hourly_xlabel":
        if re.match('hourly', self.s):    
            a = GraphLabel.hourly(self)
        #elif self.s == "daily_xlabel":
        elif re.match('daily', self.s):    
            a = GraphLabel.daily(self)
        return a
        
    def hourly(self):
        p, x, y, s, label = self.p, self.x, self.y, self.s, self.label
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        end, step, basis = label["end"], label["step"], label["basis"]
        sp_x = int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        c = 0
        for n in range(0, end, step):
            weather = p.HourlyForecast(n)
            heure = datetime.fromtimestamp(weather['dt'], tz).strftime('%H')
            #_x = x + 10 + int((w - 22) / (end - start - 1)) * n
            _x = int(sp_x + box_size_x * n + box_size_x * 0.5)
            if c % 3 == 0:
            #if int(heure) % 3 == 0:
                heure = re.sub('^0', '', heure)
                #a += SVGtools.text("middle", "16px", _x, (y - 9), "{}".format(heure)).svg()
                a += SVGtools.text("middle", "20px", _x, (y - 9), "{}".format(heure)).svg()
            c += 1
        a += '</g>'
        return a
            
    def daily(self):
        p, x, y, s, label = self.p, self.x, self.y, self.s, self.label
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        #stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        end, step, basis = label["end"], label["step"], label["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' else end
        sp_x = int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        for n in range(0, end, step):
            weather = p.DailyForecast(n)
            jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
            jour = d["abbreviated_weekday"][jour] if not d == dict() else jour
            _x = int(sp_x + box_size_x * n + box_size_x * 0.5)
            #a += SVGtools.text("middle", "16px", _x, (y - 9), "{}".format(jour)).svg()
            a += SVGtools.text("middle", "20px", _x, (y - 9), "{}".format(jour)).svg()
        a += '</g>'
        return a
        
        
class GraphPane:
    def __init__(self, p, x, y, obj):
        self.p = p
        self.x = x
        self.y = y + 90
        self.obj = obj

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
        p = self.p
        x, y = self.x, self.y
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        title = obj["title"]
        end, step, basis = obj["end"], obj["step"], obj["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" else end
        sp_x = int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])       
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 10), y=(y - h + 10), width=(w + 10), height=(h - 45), style=style).svg()
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, axis)
        # Graph
        points = str()
        c = 0
        if basis == "hour":
            tMin = min([p.HourlyForecast(n)["temp"] for n in range(0, end, step)])
            tMax = max([p.HourlyForecast(n)["temp"] for n in range(0, end, step)])
            tStep = 45 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            _title = title + ', 24 hours'
            for n in range(0, end, step):
                weather = p.HourlyForecast(n)
                #heure = datetime.fromtimestamp(h_weather['dt'], tz).strftime('%H')
                _x = int(x + box_size_x * n + box_size_x * 0.5)
                _y = y - (weather['temp'] - tMin) * tStep - 45
                points += "{},{} ".format(_x, _y)
                points2 = points + "{},{} {},{}".format(_x, (y - 35), (x + int(box_size_x * 0.5)), (y - 35))
                #if int(heure) % 3 == 0:
                if c % 3 == 0:    
                    a += SVGtools.text("end", "16px", (_x + 14), (_y - 9), "{} {}".format(round(int(weather['temp'])), p.units['temp'])).svg()
                    a += SVGtools.circle((_x), (_y - 20), 2, "black", 1, "none").svg()
                c += 1
        elif basis == "day":
            tMin = min([p.DailyForecast(n)['temp_day'] for n in range(0, end, step)])
            tMax = max([p.DailyForecast(n)['temp_day'] for n in range(0, end, step)])
            tStep = 45 / (tMax - tMin) if (tMax - tMin) != 0 else 1
            _title = '{}, {} days'.format(title, str(end))
            for n in range(0, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                jour = d["abbreviated_weekday"][jour] if not d == dict() else jour
                _x = int(x + box_size_x * n + box_size_x * 0.5)
                _y = y - (weather['temp_day'] - tMin) * tStep - 45
                points += "{},{} ".format(_x, _y)
                points2 = points + "{},{} {},{}".format(_x, (y - 35), (x + int(box_size_x * 0.5)), (y - 35))
                a += SVGtools.text("end", "16px", (_x + 14), (_y - 9), "{} {}".format(int(weather['temp_day']), p.units['temp'])).svg()
                a += SVGtools.circle((_x), (_y - 20), 2, "black", 1, "none").svg()

        style2 = "fill:{};stroke:{};stroke-width:{}px;stroke-linecap:{};".format(fill, fill, "0", stroke_linecap)
        a += SVGtools.polyline(points2, style2).svg()
        style = "fill:none;stroke:{};stroke-width:{}px;stroke-linecap:{};".format(stroke_color, stroke, stroke_linecap)
        a += SVGtools.polyline(points, style).svg()
        # Text
        a += SVGtools.text("start", "16px", x, (y - h + 26), _title).svg()
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
        end, step, basis = obj["end"], obj["step"], obj["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" else end
        sp_x = int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 10), y=(y - h + 10), width=(w + 10), height=(h - 45), style=style).svg()
        if basis == "hour" and title == "rain precipitation":
            # Graph
            th = 10.0 # threshold
            _min = min([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)]), 2)
            #_Step = step_size(_Min=_Min, _Max=_Max)
            _title = title + ', 24h'
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(0, end, step):
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
            for n in range(0, end, step):
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
                    #a += SVGtools.line(_x, _x, _y, (_y - 8), style2).svg()
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()

        # Baseline
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, 1)
        a += SVGtools.line(x1=(x - 10), x2=(x + w), y1=(y - 35), y2=(y - 35), style=style).svg()
        # Text
        #a += SVGtools.text("start", "16px", x, (y - h + 26), "{}, total: {} mm".format(_title, _Sum)).svg()
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
        end, step, basis = obj["end"], obj["step"], obj["basis"]
        end = 6 if p.config['api'] == 'TomorrowIo' and basis == "day" else end
        sp_x = int((600 - w) / 2)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 10), y=(y - h + 10), width=(w + 10), height=(h - 45), style=style).svg()
        
        if basis == "hour" and title == "snow accumulation":
            # Graph
            th = 10.0 # threshold 
            _min = min([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)]), 2)
            _title = title + ', 24h'
            style = "fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;".format(fill, stroke_color, stroke_linecap, stroke)
            for n in range(0, end, step):
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

        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, 1)
        a += SVGtools.line(x1=(x - 10), x2=(x + w), y1=(y - 35), y2=(y - 35), style=style).svg()
        # Text processing
        a += SVGtools.text("start", "16px", x, (y - h + 26), "{}, total: {} mm".format(_title, int(round(_sum)), 0)).svg()
        a += '</g>'
        return a

    def tile(self):
        p = self.p
        x, y = self.x, self.y
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
        x_sp = (600 - w) / 2
        axis_color, grid, grid_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
        title = obj["title"]
        end, step, basis = obj["end"], obj["step"], obj["basis"]
        tz = timezone(p.config['timezone'])
        a = '<g font-family="{}">\n'.format(p.config['font'])   
        # Canvas
        style = "fill:{};stroke:{};stroke-width:{}px;".format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=(x - 10), y=(y - h + 10), width=(w + 10), height=(h - 45), style=style).svg()
        style = "fill:none;stroke:{};stroke-width:{}px;".format(axis_color, axis)

        def daily_weather(p, x, y, canvas, obj):
            w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
            axis_color, grid_y, grid_y_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
            stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
            title = obj["title"]
            end, step, basis = obj["end"], obj["step"], obj["basis"]
            end = 6 if p.config['api'] == 'TomorrowIo' else end
            box_size_x = (w - (end - 1) * grid_y) / (end - 1)
            i18n = read_i18n(p, i18nfile)
            i = str()
            s = str()
            for n in range(0, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                #jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                _x = x + x_sp + int(w / end) * n
                _y = y - 45          
                i += SVGtools.transform("(1.0,0,0,1.0,{},{})".format((_x - 53), (_y - 105)), addIcon(weather['main'])).svg()
                s += SVGtools.text("start", "16px", (_x - 32), (_y - 10), "hi:").svg()
                s += SVGtools.text("end", "16px", (_x + 26), (_y - 10), "{} {}".format(round(weather['temp_max']), p.units['temp'])).svg()
                s += SVGtools.circle((_x + 15), (_y - 21), 2, "black", 1, "none").svg()
                s += SVGtools.text("start", "16px", (_x - 32), (_y + 7), "lo:").svg()
                s += SVGtools.text("end", "16px", (_x + 26), (_y + 7), "{} {}".format(round(weather['temp_min']), p.units['temp'])).svg()
                s += SVGtools.circle((_x + 15), (_y - 4), 2, "black", 1, "none").svg()
                if n < (end - 1):
                    style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_y_color, stroke_linecap, grid_y)
                    i += SVGtools.line((_x + 30), (_x + 30), (_y - h + 55), (_y + 10), style).svg()
            return s,i

        def moon_phase(p, x, y, canvas, obj):
            from hijridate import Hijri, Gregorian
            w, h, bgcolor, axis = canvas["width"], canvas["height"], canvas["bgcolor"], canvas["axis"]
            sp_x = (600 - w) / 2
            axis_color, grid_y, grid_y_color = canvas["axis_color"], canvas["grid"], canvas["grid_color"]
            stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
            title = obj["title"]
            end, step, basis = obj["end"], obj["step"], obj["basis"]
            end = 6 if p.config['api'] == 'TomorrowIo' else end
            box_size_x = (w - (end -1) * grid_y) / end
            i18n = read_i18n(p, i18nfile)
            tz = timezone(p.config['timezone'])
            ramadhan = p.config['ramadhan']
            i = str()
            s = str()           
            for n in range(0, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                day = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%-d'))
                mon = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%-m'))
                yrs = int(datetime.fromtimestamp(weather['dt'], tz).strftime('%Y'))
                lat = float(p.config['lat'])
                _x = int(sp_x + (box_size_x + grid_y) * n) 
                _y = y - 45
                r = 18 if end == 6 else 14
                # grid
                if n < (end - 1):
                    style = "fill:none;stroke:{};stroke-linecap:{};stroke-width:{}px;".format(grid_y_color, stroke_linecap, grid_y)
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55), (_y + 10), style).svg()                 
                # icon
                style = "fill:{};stroke:{};stroke-width:{}px;".format(fill, stroke_color, 1)
                i += SVGtools.circle((_x + box_size_x / 2), (_y - 53), (r + 2), stroke_color, stroke, "none").svg()

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

                def ramadhan(day, mon, yrs):
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
                rx = _x + box_size_x / 2
                ry = _y - 53
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
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                else:
                    if phase(rad) == "n":
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp +ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = "M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z".format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = ramadhan(day, mon, yrs) if ramadhan == True else str()

                i += SVGtools.path(dm, style).svg() if ps != 'f' else ''
                # moonrise and moonset time
                #t_moonrise = str(daily[20])  # test
                moonrise = "00:00" if weather['moonrise'] == 0 else str(datetime.fromtimestamp(weather['moonrise'], tz).strftime("%H:%M"))
                moonset = "00:00" if weather['moonset'] == 0 else str(datetime.fromtimestamp(weather['moonset'], tz).strftime("%H:%M"))
                s += SVGtools.text("middle", "16px", (_x + int(box_size_x * 0.5)), (_y - 10), "r: {}".format(moonrise)).svg()
                s += SVGtools.text("middle", "16px", (_x + int(box_size_x * 0.5)), (_y + 7), "s: {}".format(moonset)).svg()
                # moon phase and ramadhan 
                s += SVGtools.text("start", "16px", (_x + 3), (_y - 68), "{}".format(ps)).svg()
                s += SVGtools.text("end", "16px", (_x + box_size_x - 3), (_y - 68), "{}".format(ram)).svg()

            return s,i
        # Graph
        #points = str()
        if basis == "day" and title == "weather":
            s,i = daily_weather(p, x, y, canvas, obj)
            a += s + '</g>' + i
        elif basis == "day" and title == "moon phase":
            s,i = moon_phase(p, x, y, canvas, obj)
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

#    except Exception as e:
#        shutil.copyfile(error_image, flatten_pngfile)
#        print(e)
#        exit(1)
