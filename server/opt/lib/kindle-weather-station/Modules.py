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
            a = json.load(f)['locale'][p.config['locale']]
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



#def daytime(p, day):
#    config = p.config
#    weather = p.DailyForecast(day)
#    
#    if config['api'] == 'Tomorrow.io'
#    
#    sunrise = weather['sunrise']
#    sunset = weather['sunset']
#    now = p.now
#    tz = timezone(config['timezone'])
#    this_month = int(datetime.fromtimestamp(now, tz).strftime("%m"))


# tommorow.io
 #                               "sunriseTime": "2024-05-16T19:42:00Z",
#                                "sunsetTime": "2024-05-17T09:34:00Z",
# owm
# 'sunrise': 1715715406, 'sunset': 1715765993,

#    if not sunrise == 0:
#        d = datetime.fromtimestamp(dt, tz)
#        _, mon, day, hr, mi, _, _, _, _ = d.timetuple()
#        _dt = hr * 60 + mi
#        d = datetime.fromtimestamp(sunrise, tz)
#        yr, mon, day, hr, mi, _, _, _, _ = d.timetuple()
#        _sunrise = hr * 60 + mi
#        d = datetime.fromtimestamp(sunset, tz)
#        _, mon, day, hr, mi, _, _, _, _ = d.timetuple()
#        _sunset = hr * 60 + mi
#        if _dt > _sunrise and _dt < _sunset:
#            state = 'day'
#        else:
#            state = 'night'
#    else:
#        # The other way: Northern hemisphere: From Sep to Feb is night-time, from March to Aug is daytime, sorthern hemisphere is the exact opposite.
#        if float(config['lat']) < 0 and 3 < this_month <= 9:
#            state = 'polar_night'
#        elif float(config['lat']) < 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
#            state = 'midnight_sun'
#        elif float(config['lat']) > 0 and 3 < this_month <= 9:
#            state = 'midnight_sun'
#        elif float(config['lat']) > 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
#            state = 'polar_night'
#return state







class Maintenant:
    def __init__(self, p, y, variant=None):
        self.p = p
        self.y = y
        self.variant = variant
        
    def text(self):
        # Layout: x, y : 0, 0
        p, y = self.p, self.y
        _y = y + 40
        weather = p.CurrentWeather()
        tz = timezone(p.config['timezone'])
        now = p.now
        a = str()
        if p.config['sunrise_and_sunset'] == True:
            if weather['sunrise'] == 0:
                sunrise = "--:--"
            else:
                try:
                    sunrise = str(datetime.fromtimestamp(weather['sunrise'], tz).strftime('%H:%M'))
                except Exception as e:
                    sunrise = '--:--'
            if weather['sunset'] == 0:
                sunset = '--:--'
            else:
                try:
                    sunset = str(datetime.fromtimestamp(weather['sunset'], tz).strftime('%H:%M'))
                except Exception as e:
                    sunset = '--:--'
            # localtime
            maintenant = (str.lower(datetime.fromtimestamp(now, tz).strftime('%a, %d %b %H:%M')))
            w = maintenant.split()
            #d = read_i18n(p, i18nfile)
            #w[0] = d["abbreviated_weekday"][w[0][:-1]] + ',' if not d == dict() else w[0]
            #w[2] = d["abbreviated_month"][w[2]] if not d == dict() else w[2]
            if p.config['landscape'] == True:
                #x_date = 520
                x_date = 790
                x_city = 20
                a += SVGtools.text('start', '30px', x_city, _y, p.config['city']).svg()             
                a += SVGtools.text('end', '30px', x_date, _y, ' '.join(w)).svg()
                x_sun = 645-200+10
                _y += +200-5
                a += SVGtools.text('end', '30px', x_sun, _y, sunrise).svg()
                a += SVGtools.text('end', '30px', (x_sun + 135), _y, sunset).svg()
            else:
                x_sun = 445
                x_date = 20
                a += SVGtools.text('end', '30px', x_sun, _y, sunrise).svg()
                a += SVGtools.text('end', '30px', (x_sun + 135), _y, sunset).svg()
                a += SVGtools.text('start', '30px', x_date, _y, ' '.join(w)).svg()
        else:
            maintenant = str.lower(datetime.fromtimestamp(now, tz).strftime('%a %Y/%m/%d %H:%M'))
            w = maintenant.split()
            x_city = 20
            x_date = 580
            #d = read_i18n(p, i18nfile)
            #w[0] = d["abbreviated_weekday"][w[0]] if not d == dict() else w[0]
            a += SVGtools.text('start', '30px', x_city, _y, p.config['city']).svg()
            a += SVGtools.text('end', '30px', x_date, _y, ' '.join(w)).svg()
        return a + '</g>\n'

    def icon(self):
        p, y = self.p, self.y
        _y = y + 40
        i = str()
        if p.config['sunrise_and_sunset'] == True:
            if p.config['landscape'] == True:
                #y:-125
                _y += +200-5
                x_sun = 645-200+10
                i += SVGtools.transform('(1.1,0,0,1.1,' + str(x_sun - 117) + ',' + str(_y - 26) + ')', Icons.Sunrise()).svg() 
                i += SVGtools.transform('(1.1,0,0,1.1,' + str(x_sun + 20) + ',' + str(_y - 26) + ')', Icons.Sunset()).svg()
            else:
                x_sun = 445
                i += SVGtools.transform('(1.1,0,0,1.1,' + str(x_sun - 117) + ',' + str(_y - 26) + ')', Icons.Sunrise()).svg() 
                i += SVGtools.transform('(1.1,0,0,1.1,' + str(x_sun + 20) + ',' + str(_y - 26) + ')', Icons.Sunset()).svg()
        return i


class CurrentData:
    def precipitation(self):
        p, x, y = self.p, self.x, self.y
        config = p.config
        weather = p.CurrentWeather()
        a = str()        
        sub_main = self.sub_main
        x_main = self.x_main
        y_main = self.y_main           
        # 'in_clouds' option
        if not config['in_clouds'] == str():
            #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
            if weather['main'] in ['Cloudy']:
                r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                if r == 0:
                    a += SVGtools.text('end', '45px', (x_main + 230 - int(s_padding(r) * 0.64)), (y_main + 215), "").svg()
                else:
                    if p.config['landscape'] == True:
                        if weather['main'] == sub_main:
                            a += SVGtools.text('end', '45px', (x_main + 225 - int(s_padding(r) * 0.64)), (y_main + 240), \
                                Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                        else:
                            a += SVGtools.text('end', '40px', (x_main + 192-25 - int(s_padding(r) * 0.64)), (y_main + 200), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                    else:
                        if weather['main'] == sub_main:
                            a += SVGtools.text('end', '45px', (x_main + 225 - int(s_padding(r) * 0.64)), (y_main + 215), \
                                Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
                        else:
                            a += SVGtools.text('end', '40px', (x_main + 192 - int(s_padding(r) * 0.64)), (y_main + 200), \
                            Decimal(float(r)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).svg()
        return a

    def temperature(self):
        p, x, y, wordwrap = self.p, self.x, self.y, self.wordwrap
        weather = p.CurrentWeather()
        daily = p.DailyForecast(0)
        x_temp = self.x_temp
        y_temp = self.y_temp
        a = str()
        # Temperature
        tempEntier = math.floor(weather['temp'])
        tempDecimale = 10 * (weather['temp'] - tempEntier)
        a += SVGtools.text('end', '100px', (x_temp), (y_temp), int(tempEntier)).svg()
        a += SVGtools.text('start', '50px', (x_temp - 5), (y_temp - 5), '.' + str(int(tempDecimale))).svg()
        a += self.add_unit_temp(x=x_temp, y=y_temp, font_size=50)
        # Max temp
        a += SVGtools.text('end', '35px', (x_temp + 125), (y_temp - 40), int(math.ceil(daily['temp_max']))).svg()
        a += self.add_unit_temp(x=(x_temp + 125), y=(y_temp - 40), font_size=35)
        # Line
        a += SVGtools.line((x_temp + 65), (x_temp + 165), (y_temp - 33), (y_temp - 33), 'stroke:black;stroke-width:1px;').svg()
        # Min temp
        a += SVGtools.text('end', '35px', (x_temp + 125), (y_temp), int(math.ceil(daily['temp_min']))).svg()
        a += self.add_unit_temp(x=(x_temp + 125), y=y_temp, font_size=35)
        return a

    def add_unit_temp(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 50:
            a += SVGtools.circle((x + 6), (y - 70), 6, 'black', 3, 'none').svg()
            a += SVGtools.text('start', '35px', (x + 15), (y  - 50), p.units['temp']).svg()
        elif font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, "black", 2, "none").svg()
            a += SVGtools.text('start', '25px', (x + 10), (y  - 10), p.units['temp']).svg()
        return a

    def pressure(self):
        p = self.p
        x_text = self.x_text
        y_text = self.y_text
        weather = p.CurrentWeather()
        sp_x = -5 if p.config['api'] == 'Tomorrow.io' else 0
        a = SVGtools.text('end', '30px', (x_text + sp_x + 275),(y_text + 360), str(round(weather['pressure']))).svg()
        a+= SVGtools.text('end', '23px', (x_text + 320),(y_text + 360), p.units['pressure']).svg()
        return a

    def humidity(self):
        p = self.p
        x_text = self.x_text
        y_text = self.y_text
        weather = p.CurrentWeather()
        a = SVGtools.text('end', '30px', (x_text + 172), (y_text + 360), str(round(weather['humidity']))).svg()
        a += SVGtools.text('end', '23px', (x_text + 195), (y_text + 360), '%').svg()
        return a

    def wind(self):
        p = self.p
        x_text = self.x_text
        y_text = self.y_text
        weather = p.CurrentWeather()
        a = SVGtools.text('end', '30px', (x_text + 82),(y_text + 360), str(int(weather['wind_speed']))).svg()
        a += SVGtools.text('end', '23px', (x_text + 125),(y_text + 360), p.units['wind_speed']).svg()
        return a

    def description(self):
        p = self.p
        weather = p.CurrentWeather()
        wordwrap= self.wordwrap
        x_text = self.x_text
        y_text = self.y_text
        a = str()
        if p.config['landscape'] == True:
            wordwrap = 22
            disc = split_text(wordwrap=wordwrap, text=weather['description'], max_rows=2)
            #disc = [weather['description']]
        else:
            disc = split_text(wordwrap=wordwrap, text=weather['description'], max_rows=2)
        for w in disc:
            a += SVGtools.text('end', '30px', (x_text + 320), (y_text + 400), w).svg()
            y_text += 35
        return a

    def icon(self):
        p = self.p
        weather = p.CurrentWeather()
        sub_main = self.sub_main
        x_main = self.x_main
        y_main = self.y_main
        x_sub_main = self.x_sub_main
        y_sub_main = self.y_sub_main
        if weather['main'] == sub_main:
            return SVGtools.transform('(4,0,0,4,' + str(x_main) + ',' + str(y_main) + ')', addIcon(weather['main'])).svg()
        else:
            if p.config['landscape'] == True:
                i = str()
                i += SVGtools.transform('(3.5,0,0,3.5,' + str(x_main - 30) + ',' + str(y_main + 40) + ')', addIcon(weather['main'])).svg()
                i += SVGtools.transform('(1.6,0,0,1.6,' + str(x_sub_main + 180) + ',' + str(y_sub_main + 220) + ')', addIcon(sub_main)).svg()
                i += SVGtools.line((x_main + 275), (x_main + 215), (y_main + 220), (y_main + 280), 'stroke:black;stroke-width:2px;').svg()
            else:
                i = str()
                i += SVGtools.transform('(3.5,0,0,3.5,' + str(x_main + 10) + ',' + str(y_main + 10) + ')', addIcon(weather['main'])).svg()
                i += SVGtools.transform('(1.6,0,0,1.6,' + str(x_sub_main + 205) + ',' + str(y_sub_main + 190) + ')', addIcon(sub_main)).svg()
                i += SVGtools.line((x_main + 300), (x_main + 240), (y_main + 190), (y_main - 280), 'stroke:black;stroke-width:2px;').svg()
            return i
            
    def wind_icon(self):
        p = self.p
        x_text = self.x_text
        y_text = self.y_text
        weather = p.CurrentWeather()   
        _x = x_text - len(str(int(weather['wind_speed']))) * 17 + 40
        return SVGtools.transform('(1.6,0,0,1.6,' + str(_x) + ',' + str(y_text + 326) + ')', addIcon(weather['cardinal'])).svg()

class CurrentWeatherPane(CurrentData):
    def __init__(self, p, y, wordwrap, variant=None):
        self.p = p
        self.x = 0
        self.y = y
        self.wordwrap = wordwrap 
        self.variant = variant
        self.x_main = self.x - 25
        self.y_main = y - 90
        self.x_sub_main = self.x
        self.y_sub_main = y - 90
        self.x_temp = self.x + 160
        self.y_temp = y + 305
        self.x_text = self.x
        self.y_text = y
        weather = p.CurrentWeather()
        sunrise = weather['sunrise']
        sunset = weather['sunset']
        now = p.now
        tz = timezone(p.config['timezone'])
        this_month = int(datetime.fromtimestamp(now, tz).strftime("%m"))
        a = self.daytime(dt=now, sunrise=sunrise, sunset=sunset)
        if a == True:
            self.state = 'day'
        elif a == False:
            self.state = 'night'
        else:
            # The other way: Northern hemisphere: From Sep to Feb is night-time, from March to Aug is daytime, sorthern hemisphere is the exact opposite.
            if float(p.config['lat']) < 0 and 3 < this_month <= 9:
                self.state = 'polar_night'
            elif float(p.config['lat']) < 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
                self.state = 'midnight_sun'
            elif float(p.config['lat']) > 0 and 3 < this_month <= 9:
                self.state = 'midnight_sun'
            elif float(p.config['lat']) > 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
                self.state = 'polar_night'
               
        # Fix sub icon: ClearDay, ClearNight, PartlyCloudyDay and PartlyCloudyNight
        b = dict()       
        for n in range(24):          
            weather = p.HourlyForecast(n)
            prob = 0.98
            prob **= n
            if self.state == 'night' or self.state == 'polar_night':
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
        self.sub_main = max(b.items(), key=lambda z: z[1])[0]
        
    def text(self):
        p = self.p
        if p.config['landscape'] == True:
            self.x_text = 270
            self.y_text = -125
            prec = super(CurrentWeatherPane, self).precipitation()
            self.x_temp = 425
            self.y_temp = 185
            temp = super(CurrentWeatherPane, self).temperature()
            self.x_text = 270
            self.y_text = -85
            pres = super(CurrentWeatherPane, self).pressure()
            self.x_text = 270
            self.y_text = -85
            humi = super(CurrentWeatherPane, self).humidity()
            self.x_text = 465-200
            self.y_text = -85
            wind = super(CurrentWeatherPane, self).wind()
            #self.x_text = 270
            #self.y_text = -85
            self.x_text = 270
            self.y_text = -45-40
            disc = super(CurrentWeatherPane, self).description()
        else:
            prec = super(CurrentWeatherPane, self).precipitation()
            temp = super(CurrentWeatherPane, self).temperature() 
            pres = super(CurrentWeatherPane, self).pressure() 
            humi = super(CurrentWeatherPane, self).humidity() 
            wind = super(CurrentWeatherPane, self).wind() 
            disc = super(CurrentWeatherPane, self).description()
        a = '<g font-family="{}">\n'.format(p.config['font']) + temp + pres + humi + wind + disc + '</g>\n'
        return a

    def icon(self):
        p = self.p
        weather = p.CurrentWeather()
        if p.config['landscape'] == True:
            i = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0:
                #self.x_text = 465
                #self.y_text = -85+40
                self.x_text = 465-200
                self.y_text = -85
                i += super(CurrentWeatherPane, self).wind_icon()
        else:
            i = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0:    
                i += super(CurrentWeatherPane, self).wind_icon() 
        return i
        
    def daytime(self, dt, sunrise, sunset):
        if not sunrise == 0:
            config = self.p.config
            tz = timezone(config['timezone'])
            d = datetime.fromtimestamp(dt, tz)
            _, mon, day, hr, mi, _, _, _, _ = d.timetuple()
            _dt = hr * 60 + mi
            d = datetime.fromtimestamp(sunrise, tz)
            yr, mon, day, hr, mi, _, _, _, _ = d.timetuple()
            _sunrise = hr * 60 + mi
            d = datetime.fromtimestamp(sunset, tz)
            _, mon, day, hr, mi, _, _, _, _ = d.timetuple()
            _sunset = hr * 60 + mi
            if _dt > _sunrise and _dt < _sunset:
                return True
            else:
                return False
        else:
            return None


class HourlyWeatherPane:
    def __init__(self, p, y, hour, span, step, pitch, variant=None):
        self.p = p
        self.y = y
        self.hour = hour
        self.span = span
        self.step = step
        self.pitch = pitch
        self.variant = variant

    def text(self):
        p, y = self.p, self.y
        config = self.p.config
        hour, span, step, pitch = self.hour, self.span, self.step, self.pitch
        a = '<g font-family="{}">\n'.format(p.config['font'])
        # 3h forecast
        if p.config['landscape'] == True:
            x = 550
            for i in range(hour, span, step):
                weather = p.HourlyForecast(i)
                hrs = {3: '3 hrs', 6: '6 hrs', 9: '9 hrs'}
                a += SVGtools.text('end', '30px', (x + 200), (y + 160), round(weather['temp'])).svg()
                a += self.add_unit_temp(x=(x + 200), y=(y + 165), font_size=35)
                a += SVGtools.text('start', '30px', (x + 65), (y + 160), hrs[i]).svg()
                # 'in_clouds' option
                if not config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                        if r == 0:
                            a += SVGtools.text('end', '25px', int(x + 160 - s_padding(r) * 0.357), (y + 92-10), '').svg()
                        else:
                            a += SVGtools.text('end', '25px', int(x + 157 - s_padding(r) * 0.357), (y + 92-10), r).svg()
                y += pitch
        else:
            x = 370
            for i in range(hour, span, step):
                weather = p.HourlyForecast(i)
                hrs = {3: 'three hours', 6: 'six hours', 9: 'nine hours'}
                d = read_i18n(p, i18nfile)
                if not d == dict():
                    for k in hrs.keys():
                        hrs[k] = d['hours'][hrs[k]]
                # Hourly weather document area (base_x=370 ,base_y=40)
                a += SVGtools.text('end', '35px', (x + 30), (y + 86), round(weather['temp'])).svg()
                a += SVGtools.text('end', '25px', (x + 180), (y + 155), hrs[i]).svg()
                a += self.add_unit_temp(x=(x + 30), y=(y + 86), font_size=35)
                # 'in_clouds' option
                if not config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        r = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
                        if r == 0:
                            a += SVGtools.text('end', '25px', int(x + 140 - s_padding(r) * 0.357), (y + 92-10), '').svg()
                        else:
                            a += SVGtools.text('end', '25px', int(x + 137 - s_padding(r) * 0.357), (y + 92-10), r).svg()
                y += pitch
        return a + '</g>\n'

    def icon(self):
        p, y = self.p, self.y
        hour, span, step, pitch = self.hour, self.span, self.step, self.pitch
        i = str()
        if p.config['landscape'] == True:
            x = 550
            for n in range(hour, span, step):
                weather = p.HourlyForecast(n)
                i += SVGtools.transform('(2.3,0,0,2.3,' + str(x + 28) + ',' + str(y - 42) + ')', addIcon(weather['main'])).svg()
                y += pitch
        else:
            x = 370
            for n in range(hour, span, step):
                weather = p.HourlyForecast(n)
                i += SVGtools.transform('(2.3,0,0,2.3,' + str(x + 8) + ',' + str(y - 42) + ')', addIcon(weather['main'])).svg()
                y += pitch
        return i
        
    def add_unit_temp(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, 'black', 2, 'none').svg()
            a += SVGtools.text('start', '25px', (x + 10), (y  - 8), p.units['temp']).svg()
        return a


class DailyWeatherPane:
    def __init__(self, p, y, span, pitch, variant=None):
        self.p = p
        self.y = y
        self.pitch = 90
        self.span = 4

    def text(self):
        p, y = self.p, self.y
        day1 = p.DailyForecast(1)
        day2 = p.DailyForecast(2)
        day3 = p.DailyForecast(3)
        pitch, span = self.pitch, self.span
        tz = timezone(p.config['timezone'])
        a = '<g font-family="{}">\n'.format(p.config['font'])
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
            tMin = (int)(355 + pasTemp * (tLow - minTemp))
            tMax = (int)(440 + pasTemp * (tHigh - minTemp))
            w = str.lower(jour.strftime("%A"))
            #w = d["full_weekday"][w] if not d == dict() else w
            a += SVGtools.text('end', '35px', 200, (y + 45-20), w).svg()
            a += SVGtools.text('end', '35px', tMin, (y + 45-20), int(tLow)).svg()
            a += self.add_unit_temp(x=tMin, y=(y + 45-20), font_size=35)
            a += SVGtools.text('end', '35px', int((tMax - s_padding(tHigh))), (y + 45-20), int(tHigh)).svg()
            a += self.add_unit_temp(x=int((tMax - s_padding(tHigh))), y=(y + 45-20), font_size=35)
            style = 'stroke:black;stroke-linecap:round;stroke-width:10px;'
            a += SVGtools.line(int(tMin + 40), int(tMax - 65), (y + 35-20), (y + 35-20), style).svg()
            y += pitch
        return a + '</g>\n'

    def icon(self):
        p, y = self.p, self.y
        pitch, span = self.pitch, self.span
        i = str()
        for n in range(1, span):
            weather = p.DailyForecast(n)
            i += SVGtools.transform('(1.9,0,0,1.9,{},{})'.format(165, (y - 60-20)), addIcon(weather['main'])).svg()
            y += pitch
        return i
        
    def add_unit_temp(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, 'black', 2, 'none').svg()
            a += SVGtools.text('start', '25px', (x + 10), (y  - 8), p.units['temp']).svg()
        return a

class TwitterPane:
    def __init__(self, p, y, variant=None):
        self.p = p
        self.y = y
        self.tw = p.config['twitter']
        self.keywords = self.tw['keywords']
        
    def text(self):
        p, y, tw, keywords = self.p, self.y, self.tw, self.keywords
        #_y = int(y)
        encoding = p.config['encoding']
        #now, timezone_offset = p.now, p.timezone_offset
        a = '<g font-family="{}">\n'.format(p.config['font'])
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
        if translate == 'True':
            _b = GoogleTranslator(source='auto', target='en').translate(full_text)
            # Fix EncodeError
            en = python_encoding(encoding)
            b = _b.encode(en, 'ignore').decode(en)
        else:
            b = full_text
        c = include_keywords.split(',')
        processing = True if c == list() else False
        for n in c:
            if re.search(n, b, re.IGNORECASE):
                processing = True
                break
            else:
                processing = False
        c = exclude_keywords.split(',')
        for n in c:
            if re.search(n, b, re.IGNORECASE) and not n == str():
                processing = False
                break
        c = int()
        d_object = datetime.strptime(tweets_to_store[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        epoch = int(d_object.timestamp()) + p.timezone_offset # UTC + timezone_offset
        #print('epoch', epoch, p.now, (p.now - epoch - p.timezone_offset))
        #print('timezone offset', p.timezone_offset)
        if re.match(r'[0-9.]+m', expiration):
            c = re.sub(r'([0-9.]+)m', r'\1',expiration)
            _c = float(c) * 60
        elif re.match(r'[0-9.]+h', expiration):
            c = re.sub(r'([0-9.]+)h', r'\1',expiration)
            _c = float(c) * 60 * 60

        if p.now - epoch <= _c and processing == True:
            processing = True
        elif p.now - epoch > _c and processing == True:
            processing = False
            
        if processing == True:
            if p.config['landscape'] == True:
                if not caption == str() and not a == None:
                    a += SVGtools.text('middle', '35px', 95, (y + 35), caption).svg()
                disc = split_text(wordwrap=38, text=b, max_rows=5)
                for w in disc:
                    a += SVGtools.text('start', '30px', 180, (y + 30), w).svg()
                    y += 38
                a += '</g>\n'
            else:
                if not caption == str() and not a == None:
                    a += SVGtools.text('middle', '25px', 95, (y + 55), caption).svg()
                disc = split_text(wordwrap=36, text=b, max_rows=8)
                for w in disc:
                    a += SVGtools.text('start', '20px', 180, (y + 50), w).svg()
                    y += 25
                a += '</g>\n'
            if len(urls) > 0:
                url = urls[0]
            else:
                url = alternate_url 
        else:
            a, url = None, None
         
        return a , url, processing
        
    def draw(self, url):
        import io
        import qrcode
        import qrcode.image.svg
        #from qrcode.image.pure import PyPNGImage
        p, tw = self.p, self.tw
        multiple = 5       
        # define a method to choose which factory metho to use
        # possible values 'basic' 'fragment' 'path'
        method = 'basic'
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
        i = stream.getvalue().decode()
        # Strip unnecessary codes
        i = re.sub(r'<\?xml.+\?>\n', '', i)
        i = re.sub(r'''<svg width=[^<]+>''', '', i)
        i = re.sub(r'</svg>$', '', i)
        i = re.sub('([0-9]+)mm', r'\1', i)
        # Transformation
        if p.config['landscape'] == True:
            if not tw['caption'] == str():
                offset_x, offset_y = 8, (390 + 25)
            else:
                offset_x, offset_y = 8, 390
        else:
            if not tw['caption'] == str():
                offset_x, offset_y = 8, (560 + 25)
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
        i = re.sub(r'x="([0-9]+)"', multi_x, i)
        i = re.sub(r'y="([0-9]+)"', multi_y, i)
        i = re.sub(r'width="([0-9]+)"', multi_w, i)
        i = re.sub(r'height="([0-9]+)"', multi_h, i)
        return i    
    

class GraphLabel:
    def __init__(self, p, y, s, variant=None):
        self.p = p
        self.y = y 
        self.s = s
        self.label = p.config['graph_labels'][s]
        self.variant = variant

    def text(self):
        p = self.p
        s = self.s
        a = '<g font-family="{}">\n'.format(p.config['font'])
        #if self.s == "hourly_xlabel":
        if re.match('hourly', s):    
            a += GraphLabel.hourly(self)
        #elif self.s == "daily_xlabel":
        elif re.match('daily', s):    
            a += GraphLabel.daily(self)
        return a + '</g>\n'
        
    def hourly(self):
        p, y, s, label, variant = self.p, self.y, self.s, self.label, self.variant
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        axis_color, grid, grid_color = canvas['axis_color'], canvas['grid'], canvas['grid_color']
        start, end, step, basis, font_size = label['start'], label['end'], label['step'], label['basis'], label['font-size']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / (end - start)
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        c = 0
        for n in range(start, end, step):
            weather = p.HourlyForecast(n)
            heure = datetime.fromtimestamp(weather['dt'], tz).strftime('%H')
            _x = int(sp_x + box_size_x * n + box_size_x * 0.5)
            if c % 3 == 1:
            #if int(heure) % 3 == 0:
                heure = re.sub('^0', '', heure)
                a += SVGtools.text('middle', str(font_size) + 'px', _x, (y - 21+25), str(heure)).svg()
            c += 1
        a += '</g>'
        return a
            
    def daily(self):
        p, y, s, label, variant = self.p, self.y, self.s, self.label, self.variant
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        axis_color, grid, grid_color = canvas['axis_color'], canvas['grid'], canvas['grid_color']
        #stroke, stroke_color, fill, stroke_linecap = obj["stroke"], obj["stroke-color"], obj["fill"], obj["stroke-linecap"]
        start, end, step, basis, font_size = label['start'], label['end'], label['step'], label['basis'], label['font-size']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / (end - start)
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        for n in range(start, end, step):
            weather = p.DailyForecast(n)
            jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
            jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
            _x = int(sp_x + box_size_x * (n - start) + box_size_x * 0.5)
            a += SVGtools.text('middle', str(font_size) + 'px', _x, (y - 21+25), str(jour)).svg()
        a += '</g>'
        return a
 
class GraphLine:
    def __init__(self, p, y, obj, variant=None):
        self.p = p
        self.y = y
        self.obj = obj
        self.variant = variant
        
    def draw(self): 
        p, y, obj = self.p, self.y, self.obj 
        style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(obj['stroke-color'], obj['stroke-linecap'], obj['stroke-width'])
        i = SVGtools.line(x1=int(obj['start']), x2=int(obj['end']), y1=y, y2=y , style=style).svg()
        return i
        
class GraphPane:
    def __init__(self, p, y, obj, variant=None):
        self.p = p
        self.y = y
        self.obj = obj
        self.variant = variant

    def draw(self):
        if self.obj['type'] == 'line':
            a = self.line()
        elif self.obj['type'] == 'bar':
            a = self.bar()
        elif self.obj['type'] == 'rect':
            a = self.rect()
        elif self.obj['type'] == 'tile':
            a = self.tile()
        return a

    def line(self):
        p, y, obj = self.p, self.y, self.obj
        #x=40
        canvas = p.config['graph_canvas']
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        axis_color, grid, grid_color = canvas['axis_color'], canvas['grid'], canvas['grid_color']
        stroke, stroke_color, fill, stroke_linecap = obj['stroke'], obj['stroke-color'], obj['fill'], obj['stroke-linecap']
        start, end, step, basis, title = obj['start'], obj['end'], obj['step'], obj['basis'], obj['title']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / end
        half = box_size_x * 0.5
        a = '<g font-family="{}">\n'.format(p.config['font'])
        d = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])       
        # Canvas
        style = 'fill:{};stroke:{};stroke-width:{}px;'.format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=sp_x, y=(y - h + 140), width=w, height=(h - 45), style=style).svg()
        #style = 'stroke:{};stroke-width:{}px;'.format(axis_color, axis)
        # Graph
        points = str()
        if basis == 'hour':
            tMin = min([p.HourlyForecast(n)['temp'] for n in range(start, end, step)])
            tMax = max([p.HourlyForecast(n)['temp'] for n in range(start, end, step)])
            if p.config['landscape'] == True:
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                _title = title + ', 24 hours'
                a += SVGtools.text('start', '16px', 5, (600 - 5), _title).svg()
                c = 0
                for n in range(start, end, step):
                    weather = p.HourlyForecast(n)
                    #heure = datetime.fromtimestamp(h_weather['dt'], tz).strftime('%H')
                    _x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp'] - tMin) * tStep + 75
                    points += '{},{} '.format(_x, _y)
                    points2 = points + '{},{} {},{}'.format(_x, (y + 95), int(sp_x + half), (y + 95))
                    #if int(heure) % 3 == 0:
                    if c % 3 == 0:    
                        #a += SVGtools.text('end', '16px', (_x + 14), (_y - 9), '{} {}'.format(round(int(weather['temp'])), p.units['temp'])).svg()
                        a += SVGtools.text('middle', '25px', (_x), (_y - 14), '{} '.format(int(round(weather['temp'])))).svg()
                        a += SVGtools.circle((_x + 17), (_y - 29), 3, 'black', 2, 'none').svg()  
                    c += 1
            else:
                tStep = 35 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                _title = title + ', 24 hours'
                a += SVGtools.text('start', '16px', sp_x+5, (y - h + 156), _title).svg()
                c = 0
                for n in range(start, end, step):
                    weather = p.HourlyForecast(n)
                    #heure = datetime.fromtimestamp(h_weather['dt'], tz).strftime('%H')
                    _x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp'] - tMin) * tStep + 80
                    points += '{},{} '.format(_x, _y)
                    points2 = points + '{},{} {},{}'.format(_x, (y + 95), int(sp_x + half), (y + 95))
                    #if int(heure) % 3 == 0:
                    if c % 3 == 0:    
                        #a += SVGtools.text('end', '16px', (_x + 14), (_y - 9), '{} {}'.format(round(int(weather['temp'])), p.units['temp'])).svg()
                        a += SVGtools.text('middle', '16px', (_x), (_y - 9), '{} '.format(int(round(weather['temp'])))).svg()
                        a += SVGtools.circle((_x+10), (_y - 20), 2, 'black', 1, 'none').svg()  
                    c += 1
        elif basis == 'day':
            tMin = min([p.DailyForecast(n)['temp_day'] for n in range(start, end, step)])
            tMax = max([p.DailyForecast(n)['temp_day'] for n in range(start, end, step)])
            if p.config['landscape'] == True:
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                _title = '{}, {} days'.format(title, str(end))
                a += SVGtools.text('start', '16px', 5, (600 - 5), _title).svg()
                for n in range(start, end, step):
                    weather = p.DailyForecast(n)
                    jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                    jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
                    _x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep + 75
                    points += '{},{} '.format(_x, _y)
                    points2 = points + '{},{} {},{}'.format(_x, (y + 95), int(sp_x + half), (y + 95))
                    a += SVGtools.text('middle', '25px', (_x), (_y - 14), '{}'.format(int(weather['temp_day']))).svg()
                    #a += SVGtools.text('end', '25px', (_x + 14+10), (_y - 9-5), '{} {}'.format(int(weather['temp_day']), p.units['temp'])).svg()
                    a += SVGtools.circle((_x + 17), (_y - 29), 3, 'black', 2, 'none').svg()       
            else:
                tStep = 35 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                _title = '{}, {} days'.format(title, str(end))
                a += SVGtools.text('start', '16px', sp_x+5, (y - h + 156), _title).svg()
                for n in range(start, end, step):
                    weather = p.DailyForecast(n)
                    jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                    jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
                    _x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep + 80
                    points += '{},{} '.format(_x, _y)
                    points2 = points + '{},{} {},{}'.format(_x, (y + 95), int(sp_x + half), (y + 95))
                    #a += SVGtools.text('end', '16px', (_x + 14), (_y - 9), '{} {}'.format(int(weather['temp_day']), p.units['temp'])).svg()
                    a += SVGtools.text('middle', '16px', (_x), (_y - 9), '{} '.format(int(weather['temp_day']))).svg()
                    a += SVGtools.circle((_x + 12), (_y - 20), 2, 'black', 1, 'none').svg()         
        style2 = 'fill:{};stroke:{};stroke-width:{}px;stroke-linecap:{};'.format(fill, fill, '0', stroke_linecap)
        a += SVGtools.polyline(points2, style2).svg()
        style = 'fill:none;stroke:{};stroke-width:{}px;stroke-linecap:{};'.format(stroke_color, stroke, stroke_linecap)
        a += SVGtools.polyline(points, style).svg()
        a += '</g>'
        return a

    def bar(self):
        p, y = self.p, self.y
        #x = 40
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        axis_color, grid, grid_color = canvas['axis_color'], canvas['grid'], canvas['grid_color']
        stroke, stroke_color, fill, stroke_linecap = obj['stroke'], obj['stroke-color'], obj['fill'], obj['stroke-linecap']
        title = obj["title"]
        start, end, step, basis = obj['start'], obj['end'], obj['step'], obj['basis']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = 'fill:{};stroke:{};stroke-width:{}px;'.format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=sp_x, y=(y - h + 140), width=w, height=(h - 45), style=style).svg()
        if basis == 'hour' and title == 'rain precipitation':
            # Graph
            th = 10.0 # threshold
            _min = min([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['rainAccumulation'] for n in range(0, end, step)]), 2)
            _title = title + ', 24 hours'
            a += SVGtools.text('start', '16px', sp_x+5, (y - h + 156), '{}, total: {} mm'.format(_title, int(round(_sum)), 0)).svg()
            for n in range(start, end, step):
                weather = p.HourlyForecast(n)
                vol = weather['rainAccumulation']
                base_y = y - h + 235
                _vol = int((vol **(1/3)) * th)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(stroke_color, stroke_linecap, stroke)
                a += SVGtools.line(x1=_x, x2=_x, y1=base_y, y2=(base_y - _vol) , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16px', _x, (base_y - _vol - 10), '{} mm'.format(int(round(vol, 0)))).svg()
                    style2 = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(axis_color, stroke_linecap, '1')
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 8), style2).svg()
        elif basis == 'day' and title == 'rain precipitation':
            # Graph
            th = 5.75 # threshold
            _min = min([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _max = max([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.DailyForecast(n)['rainAccumulation'] for n in range(0, end, step)]), 2)
            _title = '{}, {} days'.format(title, str(end))
            a += SVGtools.text('start', '16px', sp_x+5, (y - h + 156), '{}, total: {} mm'.format(_title, int(round(_sum)), 0)).svg()
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                vol = weather['rainAccumulation']
                #width=25
                base_y = y - h + 235
                _vol = int((vol **(1/3)) * th)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(stroke_color, stroke_linecap, stroke)
                a += SVGtools.line(x1=_x, x2=_x, y1=base_y, y2=(base_y - _vol) , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16px', _x, (base_y - _vol - 12), '{} mm'.format(int(round(vol, 0)))).svg()
                    style2 = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(axis_color, stroke_linecap, '1')
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()

        # Baseline
        style = 'stroke:{};stroke-width:{}px;'.format(axis_color, 1)
        a += SVGtools.line(x1=(sp_x + 5), x2=(sp_x + w), y1=(y + 95), y2=(y + 95), style=style).svg()
        a += '</g>'
        return a

    def rect(self):
        p, y = self.p, self.y
        #x = 40
        canvas = p.config['graph_canvas']
        obj = self.obj
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        axis_color, grid, grid_color = canvas['axis_color'], canvas['grid'], canvas['grid_color']
        stroke, stroke_color, fill, stroke_linecap, width = obj['stroke'], obj['stroke-color'], obj['fill'], obj['stroke-linecap'], obj['width']
        title = obj['title']
        start, end, step, basis = obj['start'], obj['end'], obj['step'], obj['basis']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        box_size_x = w / end
        a = '<g font-family="{}">\n'.format(p.config['font'])
        i18n = read_i18n(p, i18nfile)
        tz = timezone(p.config['timezone'])
        # Canvas
        style = 'fill:{};stroke:{};stroke-width:{}px;'.format(bgcolor, bgcolor, (0))
        a += SVGtools.rect(x=sp_x, y=(y - h + 140), width=w, height=(h - 45), style=style).svg() 
        if basis == 'hour' and title == 'snow accumulation':
            # Graph
            th = 10.0 # threshold 
            _min = min([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _max = max([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.HourlyForecast(n)['snowAccumulation'] for n in range(0, end, step)]), 2)
            _title = title + ', 24hours'
            for n in range(start, end, step):
                weather = p.HourlyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - h + 235
                _vol = int(vol **(1/3) * th)
                #_x = sp_x + int(box_size_x * n + box_size_x * 0.5 - width * 0.5)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                style = 'fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(fill, stroke_color, stroke_linecap, stroke)
                a += SVGtools.rect(x=_x - int(width / 2), y=(base_y - _vol), width=width , height=_vol , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16px', _x, (base_y - _vol - 12), '{} mm'.format(int(round(vol, 0)))).svg()
                    style2 = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(axis_color, stroke_linecap, '1')
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()

        elif basis == 'day' and title == 'snow accumulation':
            # Graph
            th = 5.75 # threshold  
            _min = min([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _max = max([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)])
            _sum = round(sum([p.DailyForecast(n)['snowAccumulation'] for n in range(0, end, step)]), 2) 
            _title = '{}, {} days'.format(title, str(end))
            for n in range(0, end, step):
                weather = p.DailyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - h + 235
                _vol = int(vol **(1/3) * th)
                #_x = sp_x + int(box_size_x * n + box_size_x * 0.5 - width * 0.5)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                style = 'fill:{};stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(fill, stroke_color, stroke_linecap, stroke)
                a += SVGtools.rect(x=_x - int(width / 2), y=(base_y - _vol), width=width , height=_vol , style=style).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16px', _x, (base_y - _vol - 12), '{} mm'.format(int(round(vol, 0)))).svg()
                    style2 = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(axis_color, stroke_linecap, '1')
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), style2).svg()
        # Baseline
        style = 'stroke:{};stroke-width:{}px;'.format(axis_color, 1)
        #a += SVGtools.line(x1=(x - 5), x2=(x + w - 5 - grid), y1=(y + 35), y2=(y + 35), style=style).svg()
        a += SVGtools.line(x1=(sp_x + 5), x2=(sp_x + w), y1=(y + 95), y2=(y + 95), style=style).svg()
        # Text processing
        #a += SVGtools.text('start', '16px', x, (y - h + 26+70), '{}, total: {} mm'.format(_title, int(round(_sum)), 0)).svg()
        a += SVGtools.text('start', '16px', sp_x+5, (y - h + 156), '{}, total: {} mm'.format(_title, int(round(_sum)), 0)).svg()
        a += '</g>'
        return a

    def tile(self):
        p, y, obj, variant = self.p, self.y, self.obj, self.variant
        #x=40
        canvas = p.config['graph_canvas']
        grid = canvas['grid']
        basis, title = obj['basis'], obj['title']
        w, h, bgcolor, axis = canvas['width'], canvas['height'], canvas['bgcolor'], canvas['axis']
        sp_x = int((800 - w) * 0.5) if p.config['landscape'] == True else int((600 - w) * 0.5)
        kwargs = {  'w': w, 'h': h, 'bgcolor': bgcolor, 'axis': axis,
                    'axis_color': canvas['axis_color'], 'grid': canvas['grid'], 'grid_color': canvas['grid_color'],
                    'grid_ext_upper': canvas['grid_ext_upper'], 'grid_ext_lower': canvas['grid_ext_lower'],
                    'title': obj['title'], 'start': obj['start'], 'end': obj['end'], 'step': obj['step'],
                    'basis': obj['basis'], 'stroke': obj['stroke'],
                    'stroke_color': obj['stroke-color'], 'fill': obj['fill'], 'stroke_linecap': obj['stroke-linecap'],
                    'tz': timezone(p.config['timezone']), 'sp_x': sp_x, 'variant': variant}
        # Start
        a = '<g font-family="{}">\n'.format(p.config['font'])   
        # Canvas
        style = 'fill:{};stroke:{};stroke-width:{}px;'.format(bgcolor, bgcolor, 0)
        #a += SVGtools.rect(x=sp_x, y=(y - h + 80+60), width=w, height=(h - 45), style=style).svg() 
        a += SVGtools.rect(x=sp_x, y=(y - h + 140), width=w, height=(h - 45), style=style).svg()
        
        def daily_weather(p, y, w, h, bgcolor, axis, axis_color, grid, grid_color, grid_ext_upper, grid_ext_lower, \
                            stroke, stroke_color, fill, stroke_linecap, \
                            title, start, end, step, basis, tz, sp_x, variant, **kwargs):
            box_size_x = (w - (end - start - 1) * grid) / (end - start)
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p, i18nfile)
            i, s = str(), str()
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                #jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                _x = int(sp_x + (box_size_x + grid) * (n - start))
                _y = y + 90
                if p.config['landscape'] == True:
                    i += SVGtools.transform('(1.8,0,0,1.8,{},{})'.format((_x - 10), (_y - 180)), addIcon(weather['main'])).svg()
                    s += SVGtools.text('end', '30px', (_x + half), (_y + 5), '/').svg()
                    s += SVGtools.text('end', '30px', (_x + half - 20), (_y + 5), '{}'.format(round(weather['temp_min']))).svg()
                    s += SVGtools.circle((_x + half - 16), (_y - 15), 3, 'black', 2, 'none').svg()
                    s += SVGtools.text('end', '30px', (_x + half + 45), (_y + 5), '{}'.format(round(weather['temp_max']))).svg()
                    s += SVGtools.circle((_x + half + 49), (_y - 15), 3, 'black', 2, 'none').svg()
                    if n < (end - 1):
                        style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(grid_color, stroke_linecap, grid)
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55 - grid_ext_upper), (_y + 10), style).svg()
                else:
                    #i += SVGtools.transform('(1.0,0,0,1.0,{},{})'.format((_x + 12 - box_size_x * 0.5), (_y - 100)), addIcon(weather['main'])).svg()
                    sp = 0 if (end - start) == 6 else -10
                    i += SVGtools.transform('(1.0,0,0,1.0,{},{})'.format((_x - 10 + sp), (_y - 100)), addIcon(weather['main'])).svg()
                    s += SVGtools.text('end', '16px', (_x + half), (_y ), '/').svg()
                    s += SVGtools.text('end', '16px', (_x + half - 8), (_y ), '{}'.format(round(weather['temp_min']))).svg()
                    s += SVGtools.circle((_x + half - 6), (_y - 10), 2, 'black', 1, 'none').svg()
                    s += SVGtools.text('end', '16px', (_x + half + 22), (_y ), '{}'.format(round(weather['temp_max']))).svg()
                    s += SVGtools.circle((_x + half + 24), (_y - 10), 2, 'black', 1, 'none').svg()
                    #if n < (end - 1):
                    style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(grid_color, stroke_linecap, grid)
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55), (_y + 10), style).svg()
            return s,i

        def moon_phase(p, y, w, h, bgcolor, axis, axis_color, grid, grid_color, stroke, stroke_color, fill, stroke_linecap, \
                             grid_ext_upper, grid_ext_lower, title, start, end, step, basis, tz, sp_x, variant, **kwargs):
            from hijridate import Hijri, Gregorian   
            box_size_x = (w - (end - start - 1) * grid) / (end - start)
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p, i18nfile)
            ramadhan = p.config['ramadhan']
            i, s = str(),str()
            
            def calc_moonphase(day, mon, yr, half, x, y, r, lat, ramadhan, **kwargsPlus):

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

                def moonphase(day, mon, yr):
                    g = Gregorian(yr, mon, day).to_hijri()
                    _, _, d = g.datetuple()
                    mooncycle = 29.55
                    a = d / mooncycle
                    return a

                def calc_ramadhan(day, mon, yr):
                    g = Gregorian(yr, mon, day).to_hijri()
                    if g.month_name() == 'Ramadhan':
                        a = 'r'
                    else:
                        a = str()
                    return a

                # moon phase:  360d = 2pi(rad)
                #lat = -1  # test
                pi = math.pi
                #rad = weather['moon_phase'] * pi * 2  
                # One call API: 0 or 1:new moon, 0.25:first qurater moon, 0.5:full moon, 0.75:third quarter moon 
                m = moonphase(day, mon, yr)
                rad = m * pi * 2 if m <= 1 else pi * 2  # hijridate module
                c = 0.025
                m = rad * c * math.cos(rad)
                #rx = _x - 3
                rx = x + half
                ry = y + 7
                rp = r + 2
                #rp = r - 2 # test
                ra1 = 1 * rp
                ra2 = (math.cos(rad) * rp)
                ra3 = 1 * rp
                if lat >= 0:
                    if phase(rad) == 'n':
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m ) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                else:
                    if phase(rad) == 'n':
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif rad < pi * 0.5:
                        px1 = math.cos(pi * 1.5 - m) * rp + rx
                        py1 = math.sin(pi * 1.5 - m) * rp + ry
                        px2 = math.cos(pi * 1.5 - m) * rp + rx
                        py2 = -math.sin(pi * 1.5 - m) * rp +ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif pi > rad >= pi * 0.5:
                        px1 = math.cos(pi * 1.5 + m) * rp + rx
                        py1 = math.sin(pi * 1.5 + m) * rp + ry
                        px2 = math.cos(pi * 1.5 + m) * rp + rx
                        py2 = -math.sin(pi * 1.5 + m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    elif pi * 1.5 > rad >= pi:
                        px1 = math.cos(pi * 0.5 + m) * rp + rx
                        py1 = math.sin(pi * 0.5 + m) * rp + ry
                        px2 = math.cos(pi * 0.5 + m) * rp + rx
                        py2 = -math.sin(pi * 0.5 + m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 0 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                    else:
                        px1 = math.cos(pi * 0.5 - m) * rp + rx
                        py1 = math.sin(pi * 0.5 - m) * rp + ry
                        px2 = math.cos(pi * 0.5 - m) * rp + rx
                        py2 = -math.sin(pi * 0.5 - m) * rp + ry
                        dm = 'M{} {} A{} {} 0 1 1 {} {} {} {} 0 0 1 {} {}z'.format(px1, py1, ra1, ra1, px2, py2, ra2, ra3+1.75, px1, py1)
                        ps = phase(rad)
                        ram = calc_ramadhan(day, mon, yr) if ramadhan == True else str()
                return dm, ps, ram
                
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                yr, mon, day, _, _, _, _, _, _ = datetime.fromtimestamp(weather['dt'], tz).timetuple()  
                lat = float(p.config['lat'])
                moonrise = '--:--' if weather['moonrise'] == 0 else str(datetime.fromtimestamp(weather['moonrise'], tz).strftime('%H:%M'))
                moonset = '--:--' if weather['moonset'] == 0 else str(datetime.fromtimestamp(weather['moonset'], tz).strftime('%H:%M'))                
                if p.config['landscape'] == True:
                    _x = int(sp_x + (box_size_x + grid) * n) 
                    _y = y - 10
                    # grid
                    if n < (end - 1):
                        style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(grid_color, stroke_linecap, grid)
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 150 - grid_ext_upper), (_y + 105), style).svg()                 
                    # Moon icon
                    r = 25
                    kwargsPlus = {'day': day, 'mon': mon, 'yr': yr, 'lat': lat, 'x': _x, 'y': _y, 'r': r, 'half': half, 'ramadhan': ramadhan}
                    dm, ps, ram = calc_moonphase(**kwargsPlus)
                    style = 'fill:{};stroke:{};stroke-width:{}px;'.format(fill, stroke_color, 1)
                    i += SVGtools.circle((_x + half), (_y + 7), (r + 2), stroke_color, (stroke + 1), 'none').svg()
                    i += SVGtools.path(dm, style).svg() if ps != 'f' else ''
                    # Text: moonrise and moonset
                    s += SVGtools.text('middle', '25px', (_x + half), (_y + 80), moonrise).svg()
                    s += SVGtools.text('middle', '25px', (_x + half), (_y + 103), moonset).svg()
                    # Text: moon phase and ramadhan
                    d = {'n': 'new', '1': 'first', 'f': 'full', '3': 'last'}
                    ps = d[ps] if ps in d else str()
                    ram = 'ram' if ram == 'r' else str()
                    if not ps == str() and not ram == str():
                        s += SVGtools.text2('middle', 'bold', '18px', (_x + half), (_y - 30), '{},{}'.format(ps, ram)).svg()
                    elif ps == str() and not ram == str():
                        s += SVGtools.text2('middle', 'bold', '18px', (_x + half), (_y - 30), '{}'.format(ram)).svg()
                    else:
                        s += SVGtools.text2('middle', 'bold', '18px', (_x + half), (_y - 30), '{}'.format(ps)).svg()
                else:
                    _x = int(sp_x + (box_size_x + grid) * (n - start)) 
                    _y = y + 25  
                    r = 18 if end == 6 else 14
                    #if n < (end - 1):
                    style = 'stroke:{};stroke-linecap:{};stroke-width:{}px;'.format(grid_color, stroke_linecap, grid)
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 115), (_y + 70), style).svg()                 
                    # Moon icon
                    kwargsPlus = {'day': day, 'mon': mon, 'yr': yr, 'lat': lat, 'x': _x, 'y': _y, 'r': r, 'half': half, 'ramadhan': ramadhan}
                    dm, ps, ram = calc_moonphase(**kwargsPlus)
                    style = 'fill:{};stroke:{};stroke-width:{}px;'.format(fill, stroke_color, 1)
                    i += SVGtools.circle((_x + box_size_x / 2), (_y + 7), (r + 2), stroke_color, stroke, "none").svg()
                    i += SVGtools.path(dm, style).svg() if ps != 'f' else ''
                    # Text: moonrise and moonset
                    s += SVGtools.text('middle', '16px', (_x + int(box_size_x * 0.5)), (_y + 50), moonrise).svg()
                    s += SVGtools.text('middle', '16px', (_x + int(box_size_x * 0.5)), (_y + 68), moonset).svg()
                    style = 'stroke:black;stroke-width:1px;'
                    i += SVGtools.line((_x + half - 25), (_x  + half + 25), (_y + 54), (_y + 54), style).svg()
                    # Text: moon phase and ramadhan 
                    s += SVGtools.text('start', '16px', (_x + 3), (_y - 8), '{}'.format(ps)).svg()
                    s += SVGtools.text('end', '16px', (_x + box_size_x - 3), (_y - 8), '{}'.format(ram)).svg()      
            return s,i
        # Graph
        if basis == 'day' and title == 'weather':
            s,i = daily_weather(p, y, **kwargs)
            a += s + '</g>' + i
        elif basis == 'day' and title == 'moon phase':
            s,i = moon_phase(p, y, **kwargs)
            if p.config['landscape'] == True:
                s += SVGtools.text('start', '16px', 10, (600 - 5), 'moon phase').svg()
            #else:
            #    s += SVGtools.text('start', '16px', 40, (800 - 5), 'moon phase').svg()
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

