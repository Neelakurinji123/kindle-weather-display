#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Date       : 24 April 2024 


import time as t
import sys, re, math, json, os, pathlib, io
from datetime import datetime, timedelta, date
import zoneinfo
import locale
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
import SVGtools
import Icons

if os.path.exists('./IconExtras.py'):
    import IconExtras as IconExtras
else:
    def IconExtras():
        return str()
        
def s_padding(x):
    if x >= 100 : return -5
    elif 100 > x >= 10 : return 10
    elif 10 > x >= 0 : return 30
    elif -10 < x < 0 : return 20
    elif x <= -10 : return 0

def read_i18n(p):
    filename = p.config['i18n_file']
    with open(filename, 'r') as f:
        try:
            a = json.load(f)['locale'][p.config['locale']]
        except:
            a = dict()
    return a
    
def split_text(wordwrap, text, max_rows):
    a, s = list(), list()
    d = dict()
    max_rows -= 1
    rows = 0
    if wordwrap == -1:
        return text
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

def fix_text(w):
    w = re.sub(r'\&','&amp;', w)
    w = re.sub(r'\<','&lt;', w)
    w = re.sub(r'\>','&gt;', w)
    return w

def python_encoding(encoding):
    # convert Unix encoding to python encoding
    encoding_list={'us-ascii': 'ascii', 'iso-8859-1': 'latin_1', 'iso8859-1': 'latin_1', 'cp819': 'latin_1', \
                        'iso-8859-2': 'iso8859_2', 'iso-8859-4': 'iso8859_4', 'iso-8859-5': 'iso8859_5', \
                        'iso-8859-6': 'iso8859_6', 'iso-8859-7': 'iso8859_7', 'iso-8859-8': 'iso8859_8', \
                        'iso-8859-9': 'iso8859_9', 'iso-8859-10': 'iso8859_10', 'iso-8859-11': 'iso8859_11', \
                        'iso-8859-13': 'iso8859_13', 'iso-8859-14': 'iso8859_14', 'iso-8859-15': 'iso8859_15', \
                        'iso-8859-16': 'iso8859_16', 'utf8': 'utf_8'}
    return encoding_list[encoding]

def daytime(p, dt, sunrise, sunset):
    # calculate daytime
    this_month = int(datetime.fromtimestamp(p.now, p.config['tz']).strftime("%m"))
    if not sunrise == 0:
        d = datetime.fromtimestamp(dt, p.config['tz'])
        _, _, _, hr, mi, _, _, _, _ = d.timetuple()
        _dt = hr * 60 + mi
        d = datetime.fromtimestamp(sunrise, p.config['tz'])
        _, _, _, hr, mi, _, _, _, _ = d.timetuple()
        _sunrise = hr * 60 + mi
        d = datetime.fromtimestamp(sunset, p.config['tz'])
        _, _, _, hr, mi, _, _, _, _ = d.timetuple()
        _sunset = hr * 60 + mi
        if _dt > _sunrise and _dt < _sunset:
            state = 'day'
        else:
            state = 'night'
    else:
        # The other way: Northern hemisphere: From Sep to Feb is night-time, from March to Aug is daytime, sorthern hemisphere is the exact opposite.
        if float(p.config['lat']) < 0 and 3 < this_month <= 9:
            state = 'polar_night'
        elif float(p.config['lat']) < 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
            state = 'midnight_sun'
        elif float(p.config['lat']) > 0 and 3 < this_month <= 9:
            state = 'midnight_sun'
        elif float(p.config['lat']) > 0 and (0 < this_month <= 3 or 9 < this_month <= 12):
            state = 'polar_night'
    return state

def dark_mode(p, dt, sunrise, sunset):
    if p.config['darkmode'] == 'True':
        darkmode = True
    elif p.config['darkmode'] == 'Auto':
        state = daytime(p, dt, sunrise, sunset)
        if state == 'night' or state == 'polar_night':
            darkmode = True
        else:
            darkmode = False
    else:
        darkmode = False
    return darkmode

class Maintenant:
    def __init__(self, p, y):
        self.p = p
        self.y = y
        self.font_family = self.p.config['font']
        
    def text(self):
        y = self.y + 40
        weather = self.p.CurrentWeather()
        tz = self.p.config['tz']
        a = str()
        if self.p.config['sunrise_and_sunset'] == True:
            if weather['sunrise'] == 0:
                sunrise = "--:--"
            else:
                try:
                    sunrise = str(datetime.fromtimestamp(weather['sunrise'], tz).strftime('%-H:%M'))
                except Exception as e:
                    sunrise = '--:--'
            if weather['sunset'] == 0:
                sunset = '--:--'
            else:
                try:
                    sunset = str(datetime.fromtimestamp(weather['sunset'], tz).strftime('%-H:%M'))
                except Exception as e:
                    sunset = '--:--'
            # localtime
            if self.p.config['landscape'] == True:
                maintenant = (str.lower(datetime.fromtimestamp(self.p.now, tz).strftime('%A, %d %B %-H:%M')))
            else:
                maintenant = (str.lower(datetime.fromtimestamp(self.p.now, tz).strftime('%a, %d %b %-H:%M')))
            w = maintenant.split()
            #d = read_i18n(self.p)
            #w[0] = d["abbreviated_weekday"][w[0][:-1]] + ',' if not d == dict() else w[0]
            #w[2] = d["abbreviated_month"][w[2]] if not d == dict() else w[2]
            if self.p.config['landscape'] == True:
                x_sun = 540
                x_date = 20            
                a += SVGtools.text('start', '30', x_date, y, ' '.join(w)).svg()
                a += SVGtools.text('start', '30', x_sun, y, sunrise).svg()
                a += SVGtools.text('start', '30', (x_sun + 125), y, sunset).svg()
                # moon icon
                d = dark_mode(self.p, self.p.now, weather['sunrise'], weather['sunset'])
                if d == True:
                    fg_color = 'rgb(255,255,255)'
                    bg_color = 'rgb(0,0,0)'
                else:
                    fg_color = 'rgb(0,0,0)'
                    bg_color = 'rgb(255,255,255)'
                x_moon = 775
                r = 10
                yr, mon, day, _, _, _, _, _, _ = datetime.now().timetuple()
                kw = {'p': self.p, 'day': day, 'mon': mon, 'yr': yr, 'lat': float(self.p.config['lat']), 'rx': x_moon, 'ry': (y - 10), 'r': r, 'ramadhan': self.p.config['ramadhan']}
                a += SVGtools.circle(x_moon, (y - 10), r, fg_color, 3, fg_color).svg()
                m = Moonphase(**kw)
                dm, ps, ram = m.calc()
                style = f'fill:{bg_color};stroke:{bg_color};stroke-width:0px;'
                a += m.svg(dm=dm, ps=ps, stroke_color=bg_color, r_plus=1, stroke=0, style=style)
            else:
                x_sun = 365
                x_date = 20
                a += SVGtools.text('start', '30', x_sun, y, sunrise).svg()
                a += SVGtools.text('start', '30', (x_sun + 135), y, sunset).svg()
                a += SVGtools.text('start', '30', x_date, y, ' '.join(w)).svg()
        else:
            maintenant = str.lower(datetime.fromtimestamp(self.p.now, tz).strftime('%a %Y/%m/%d %-H:%M'))
            w = maintenant.split()
            #d = read_i18n(self.p)
            #w[0] = d["abbreviated_weekday"][w[0]] if not d == dict() else w[0]
            x_city = 20
            x_date = 580
            a += SVGtools.text('start', '30', x_city, y, self.p.config['city']).svg()
            a += SVGtools.text('end', '30', x_date, y, ' '.join(w)).svg()
        svg = SVGtools.fontfamily(font=self.font_family, _svg=a).svg()
        return svg

    def icon(self):
        i = str()
        if self.p.config['sunrise_and_sunset'] == True:
            if self.p.config['landscape'] == True:
                x_sunrise = 503
                x_sunset = x_sunrise + 127
                y_sun = self.y + 14
            else:
                x_sunrise = 328
                x_sunset = x_sunrise + 137
                y_sun = self.y + 14               
            i += SVGtools.transform(f'(1.1,0,0,1.1,{x_sunrise},{y_sun})', Icons.Sunrise()).svg()     
            i += SVGtools.transform(f'(1.1,0,0,1.1,{x_sunset},{y_sun})', Icons.Sunset()).svg()
        return i


class CurrentData:
    def precipitation(self):
        weather = self.p.CurrentWeather()
        a = str()           
        # 'in_clouds' option: cloudCover, probability
        if not self.p.config['in_clouds'] == str():
            #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
            if weather['main'] in ['Cloudy']:
                v = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                padding = int(s_padding(v) * 0.64)
                if v == 0:
                    a += SVGtools.text('end', '45', (self.x_main + 230 - padding), (self.y_main + 215), "").svg()
                else:
                    if self.p.config['landscape'] == True:
                        if weather['main'] == self.sub_main:
                            a += SVGtools.text('end', '45', (self.x_main + 225 - padding), (self.y_main + 247), v).svg()
                        else:
                            a += SVGtools.text('end', '40', (self.x_main + 185 - padding), (self.y_main + 232), v).svg()
                    else:
                        if weather['main'] == self.sub_main:
                            a += SVGtools.text('end', '45', (self.x_main + 225 - padding), (self.y_main + 215), v).svg()
                        else:
                            a += SVGtools.text('end', '40', (self.x_main + 210 - padding), (self.y_main + 200), v).svg()
        return a

    def temperature(self):
        weather = self.p.CurrentWeather()
        daily = self.p.DailyForecast(0)
        style_line = 'stroke:black;stroke-width:1px;'
        a = str()
        # Temperature
        tempEntier = math.floor(weather['temp'])
        tempDecimale = 10 * (weather['temp'] - tempEntier)
        a += SVGtools.text('end', '100', (self.x_temp - 10), (self.y_temp), int(tempEntier)).svg()
        a += SVGtools.text('start', '50', (self.x_temp - 5), (self.y_temp - 5), '.' + str(int(tempDecimale))).svg()
        a += self.add_unit_temp(x=self.x_temp, y=self.y_temp, font_size=50)
        # Max temp
        a += SVGtools.text('end', '35', (self.x_temp + 113), (self.y_temp - 40), int(math.ceil(daily['temp_max']))).svg()
        a += self.add_unit_temp(x=(self.x_temp + 115), y=(self.y_temp - 40), font_size=35)
        # Line
        a += SVGtools.line((self.x_temp + 55), (self.x_temp + 155), (self.y_temp - 33), (self.y_temp - 33), style_line).svg()
        # Min temp
        a += SVGtools.text('end', '35', (self.x_temp + 113), (self.y_temp), int(math.ceil(daily['temp_min']))).svg()
        a += self.add_unit_temp(x=(self.x_temp + 115), y=self.y_temp, font_size=35)
        return a

    def add_unit_temp(self, x, y, font_size):
        a = str()
        if font_size == 50:
            a += SVGtools.circle((x + 6), (y - 70), 6, 'black', 3, 'none').svg()
            a += SVGtools.text('start', '35', (x + 15), (y  - 50), self.p.units['temp']).svg()
        elif font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, 'black', 2, 'none').svg()
            a += SVGtools.text('start', '25', (x + 10), (y  - 10), self.p.units['temp']).svg()
        return a

    def pressure(self):
        weather = self.p.CurrentWeather()
        sp_x = -5 if self.p.config['api'] == 'Tomorrow.io' else 0
        a = SVGtools.text('end', '30', (self.x_text + sp_x + 275),(self.y_text + 360), str(round(weather['pressure']))).svg()
        a+= SVGtools.text('end', '23', (self.x_text + 320),(self.y_text + 360), self.p.units['pressure']).svg()
        return a

    def humidity(self):
        weather = self.p.CurrentWeather()
        if self.p.config['landscape'] == True:
            a = SVGtools.text('end', '30', (self.x_text + 295), (self.y_text + 320), str(round(weather['humidity']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 320), (self.y_text + 320), '%').svg()
        else:
            a = SVGtools.text('end', '30', (self.x_text + 172), (self.y_text + 360), str(round(weather['humidity']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 195), (self.y_text + 360), '%').svg()
        return a

    def wind(self):
        weather = self.p.CurrentWeather()
        weather['cardinal'] = str() if int(weather['wind_speed']) == 0 else weather['cardinal']
        if self.p.config['landscape'] == True and self.p.config['wind_icon'] == True:
            a = SVGtools.text('end', '30', (self.x_text + 174),(self.y_text + 320), str(int(weather['wind_speed']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 217),(self.y_text + 320), self.p.units['wind_speed']).svg()
        elif self.p.config['landscape'] == True and self.p.config['wind_icon'] == False:
            a = SVGtools.text('end', '30', (self.x_text + 174),(self.y_text + 320), weather['cardinal'].lower() + ' ' + str(int(weather['wind_speed']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 217),(self.y_text + 320), self.p.units['wind_speed']).svg()
        elif self.p.config['wind_icon'] == False:
            a = SVGtools.text('end', '30', (self.x_text + 82),(self.y_text + 360), weather['cardinal'].lower() + ' ' + str(int(weather['wind_speed']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 125),(self.y_text + 360), self.p.units['wind_speed']).svg()
        else:
            a = SVGtools.text('end', '30', (self.x_text + 82),(self.y_text + 360), str(int(weather['wind_speed']))).svg()
            a += SVGtools.text('end', '23', (self.x_text + 125),(self.y_text + 360), self.p.units['wind_speed']).svg()
        return a

    def description(self):
        weather = self.p.CurrentWeather()
        y_text = self.y_text
        a = str()
        if self.p.config['landscape'] == True:
            self.wordwrap = 22
            disc = split_text(wordwrap=self.wordwrap, text=weather['description'].lower(), max_rows=2)
        else:
            disc = split_text(wordwrap=self.wordwrap, text=weather['description'].lower(), max_rows=2)
        for w in disc:
            a += SVGtools.text('end', '30', (self.x_text + 320), (y_text + 400), w).svg()
            y_text += 35
        return a

    def icon(self):
        weather = self.p.CurrentWeather()
        style_line = 'stroke:black;stroke-width:2px;'
        if weather['main'] == self.sub_main:
            if self.p.config['landscape'] == True:
                self.y_main += 25
                return SVGtools.transform(f'(4,0,0,4,{self.x_main},{self.y_main})', addIcon(weather['main'])).svg()
            else:
                return SVGtools.transform(f'(4,0,0,4,{self.x_main},{self.y_main})', addIcon(weather['main'])).svg()
        else:
            if self.p.config['landscape'] == True:
                i = str()
                self.x_main += -5
                self.y_main += 40
                i += SVGtools.transform(f'(3.5,0,0,3.5,{self.x_main},{self.y_main})', addIcon(weather['main'])).svg()
                self.x_sub_main += 180
                self.y_sub_main += 215
                i += SVGtools.transform(f'(1.6,0,0,1.6,{self.x_sub_main},{self.y_sub_main})', addIcon(self.sub_main)).svg()
                i += SVGtools.line((self.x_main + 295), (self.x_main + 235), (self.y_main + 180), (self.y_main + 270), style_line).svg()
            else:
                i = str()
                self.x_main += 10
                self.y_main += 10
                i += SVGtools.transform(f'(3.5,0,0,3.5,{self.x_main},{self.y_main})', addIcon(weather['main'])).svg()
                self.x_sub_main += 205
                self.y_sub_main += 190
                i += SVGtools.transform(f'(1.6,0,0,1.6,{self.x_sub_main},{self.y_sub_main})', addIcon(self.sub_main)).svg()
                i += SVGtools.line((self.x_main + 285), (self.x_main + 225), (self.y_main + 190), (self.y_main + 280), style_line).svg()
            return i
            
    def wind_icon(self):
        weather = self.p.CurrentWeather()   
        _x = self.x_text - len(str(int(weather['wind_speed']))) * 17 + 40
        if self.p.config['landscape'] == True:
            x_wind = _x + 92
            y_wind = self.y_text + 286
            return SVGtools.transform(f'(1.6,0,0,1.6,{x_wind},{y_wind})', addIcon(weather['cardinal'])).svg()
        else:
            x_wind = _x
            y_wind = self.y_text + 326
            return SVGtools.transform(f'(1.6,0,0,1.6,{x_wind},{y_wind})', addIcon(weather['cardinal'])).svg()

class CurrentWeatherPane(CurrentData):
    def __init__(self, p, y=0, wordwrap=-1):
        self.p = p
        self.x = 0
        self.y = y
        self.wordwrap = wordwrap 
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
        self.state = daytime(p=p, dt=p.now, sunrise=sunrise, sunset=sunset)
        b = dict()
        # fix icons     
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
        # genarate main info pane
        if self.p.config['landscape'] == True:
            self.x_text = 260
            self.y_text = -125
            prec = super(CurrentWeatherPane, self).precipitation()
            self.x_temp = 415
            self.y_temp = 185
            temp = super(CurrentWeatherPane, self).temperature()
            self.x_text = 250
            self.y_text = -85
            pres = super(CurrentWeatherPane, self).pressure()
            self.x_text = 250
            humi = super(CurrentWeatherPane, self).humidity()
            self.x_text = 260
            wind = super(CurrentWeatherPane, self).wind()
            self.x_text = 250
            disc = super(CurrentWeatherPane, self).description()
        else:
            prec = super(CurrentWeatherPane, self).precipitation()
            temp = super(CurrentWeatherPane, self).temperature() 
            pres = super(CurrentWeatherPane, self).pressure() 
            humi = super(CurrentWeatherPane, self).humidity() 
            wind = super(CurrentWeatherPane, self).wind() 
            disc = super(CurrentWeatherPane, self).description()
        a = SVGtools.fontfamily(font=self.p.config['font'], _svg=prec + temp + pres + humi + wind + disc).svg()
        return a

    def icon(self):
        weather = self.p.CurrentWeather()
        if self.p.config['landscape'] == True:
            self.x_main += -15
            i = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0 and self.p.config['wind_icon'] == True:
                self.x_text = 255
                self.y_text = -85
                i += super(CurrentWeatherPane, self).wind_icon()
        else:
            i = super(CurrentWeatherPane, self).icon()
            if int(weather['wind_speed']) != 0 and self.p.config['wind_icon'] == True:    
                i += super(CurrentWeatherPane, self).wind_icon() 
        return i


class HourlyWeatherPane:
    def __init__(self, p, y, hour, span, step, pitch):
        self.p = p
        self.y = y
        self.hour = hour
        self.span = span
        self.step = step
        self.pitch = pitch

    def text(self):
        y = self.y
        hrs = {3: 'three hours', 6: 'six hours', 9: 'nine hours'}
        d = read_i18n(self.p)
        a = str()
        # 3hr forecast
        if self.p.config['landscape'] == True:
            x = 550
            for i in range(self.hour, self.span, self.step):
                weather = self.p.HourlyForecast(i)
                a += SVGtools.text('end', '35', (x + 200), (y + 90), round(weather['temp'])).svg()
                a += self.add_unit_temp(x=(x + 200), y=(y + 90), font_size=35)
                a += SVGtools.text('start', '30', (x + 55), (y + 160), hrs[i]).svg()
                # 'in_clouds' option: cloudCover, probability
                if not self.p.config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        v = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                        if v == 0:
                            a += SVGtools.text('end', '25', int(x + 160 - s_padding(v) * 0.357), (y + 82), '').svg()
                        else:
                            a += SVGtools.text('end', '25', int(x + 122 - s_padding(v) * 0.357), (y + 82), v).svg()
                y += self.pitch
        else:
            x = 370
            for i in range(self.hour, self.span, self.step):
                weather = self.p.HourlyForecast(i)
                if not d == dict():
                    for k in hrs.keys():
                        hrs[k] = d['hours'][hrs[k]]
                a += SVGtools.text('end', '35', (x + 30), (y + 86), round(weather['temp'])).svg()
                a += SVGtools.text('end', '25', (x + 180), (y + 155), hrs[i]).svg()
                a += self.add_unit_temp(x=(x + 30), y=(y + 86), font_size=35)
                # 'in_clouds' option: cloudCover, probability
                if not self.p.config['in_clouds'] == str():
                    #if weather['main'] in ['Rain', 'Drizzle', 'Snow', 'Sleet', 'Cloudy']:
                    if weather['main'] in ['Cloudy']:
                        v = Decimal(weather['in_clouds']).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                        if v == 0:
                            a += SVGtools.text('end', '25', int(x + 140 - s_padding(v) * 0.357), (y + 82), '').svg()
                        else:
                            a += SVGtools.text('end', '25', int(x + 137 - s_padding(v) * 0.357), (y + 82), v).svg()
                y += self.pitch
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()

    def icon(self):
        y = self.y
        i = str()
        c_weather = self.p.CurrentWeather()
        sunrise = c_weather['sunrise']
        sunset = c_weather['sunset']
        state = daytime(p=self.p, dt=self.p.now, sunrise=sunrise, sunset=sunset)
        if self.p.config['landscape'] == True:
            x = 550
            y += -30
            for n in range(self.hour, self.span, self.step):
                weather = self.p.HourlyForecast(n)
                # tweak weather icon
                if state == 'polar_night' and re.search('Day', weather['main']):
                    weather['main'] = re.sub('Day', 'Night', weather['main'])
                elif state == 'midnight_sun' and re.search('Night', weather['main']):
                    weather['main'] = re.sub('Night', 'Day', weather['main'])
                i += SVGtools.transform(f'(2.0,0,0,2.0,{x},{y})', addIcon(weather['main'])).svg()
                y += self.pitch
        else:
            x = 378
            y += -42
            for n in range(self.hour, self.span, self.step):
                weather = self.p.HourlyForecast(n)
                # tweak weather icon
                if state == 'polar_night' and re.search('Day', weather['main']):
                    weather['main'] = re.sub('Day', 'Night', weather['main'])
                elif state == 'midnight_sun' and re.search('Night', weather['main']):
                    weather['main'] = re.sub('Night', 'Day', weather['main'])
                i += SVGtools.transform(f'(2.3,0,0,2.3,{x},{y})', addIcon(weather['main'])).svg()
                y += self.pitch
        return i
        
    def add_unit_temp(self, x, y, font_size):
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, 'black', 2, 'none').svg()
            a += SVGtools.text('start', '25', (x + 10), (y  - 8), self.p.units['temp']).svg()
        return a

class DailyWeatherPane:
    def __init__(self, p, y, span, pitch):
        self.p = p
        self.y = y
        self.pitch = 90
        self.span = 4

    def text(self):
        y = self.y
        day1 = self.p.DailyForecast(1)
        day2 = self.p.DailyForecast(2)
        day3 = self.p.DailyForecast(3)
        tz = self.p.config['tz']
        style_temp = 'stroke:black;stroke-linecap:round;stroke-width:10px;'
        a = str()
        # get max and min temp
        minTemp = math.floor(min([day1['temp_min'], day2['temp_min'], day3['temp_min']]))
        maxTemp = math.ceil(max([day1['temp_max'], day2['temp_max'] , day3['temp_max']]))
        pasTemp = 120 / (maxTemp-minTemp)
        d = read_i18n(self.p)
        # draw temp x-bars
        for i in range(1, self.span):
            weather = self.p.DailyForecast(i)
            tLow = math.floor(weather['temp_min'])
            tHigh = math.ceil(weather['temp_max'])
            jour = datetime.fromtimestamp(weather['dt'], tz)
            tMin = (int)(355 + pasTemp * (tLow - minTemp))
            tMax = (int)(440 + pasTemp * (tHigh - minTemp))
            w = str.lower(jour.strftime("%A"))
            #w = d["full_weekday"][w] if not d == dict() else w
            a += SVGtools.text('end', '35', 200, (y + 30), w).svg()
            a += SVGtools.text('end', '35', tMin, (y + 30), int(tLow)).svg()
            a += self.add_unit_temp(x=tMin, y=(y + 30), font_size=35)
            a += SVGtools.text('end', '35', int((tMax - s_padding(tHigh))), (y + 30), int(tHigh)).svg()
            a += self.add_unit_temp(x=int((tMax - s_padding(tHigh))), y=(y + 30), font_size=35)
            a += SVGtools.line(int(tMin + 40), int(tMax - 65), (y + 18), (y + 18), style_temp).svg() 
            y += self.pitch
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()

    def icon(self):
        y = self.y
        i = str()
        x = 165
        y += -75
        for n in range(1, self.span):
            weather = self.p.DailyForecast(n)
            # tweak weather icon
            dt = weather['dt']
            sunrise = weather['sunrise']
            sunset = weather['sunset']
            state = daytime(p=self.p, dt=dt, sunrise=sunrise, sunset=sunset)
            if state == 'polar_night' and re.search('Day', weather['main']):
                weather['main'] = re.sub('Day', 'Night', weather['main'])
            elif state == 'midnight_sun' and re.search('Night', weather['main']):
                weather['main'] = re.sub('Night', 'Day', weather['main'])
            
            i += SVGtools.transform(f'(1.9,0,0,1.9,{x},{y})', addIcon(weather['main'])).svg()
            y += self.pitch
        return i
        
    def add_unit_temp(self, x, y, font_size):
        p = self.p
        a = str()
        if font_size == 35:
            a += SVGtools.circle((x + 5), (y - 23), 4, 'black', 2, 'none').svg()
            a += SVGtools.text('start', '25', (x + 10), (y  - 8), p.units['temp']).svg()
        return a

class TwitterPane:
    def __init__(self, p, y):
        self.p = p
        self.y = y
        self.tw = p.config['twitter']
        self.keywords = self.tw['keywords']
        
    def text(self):
        y, tw, keywords = self.y, self.tw, self.keywords
        encoding = self.p.config['encoding']
        a = str()
        from twikit import Client
        from deep_translator import GoogleTranslator
        screen_name, caption, translate, translate_target = tw['screen_name'], tw['caption'], tw['translate'], tw['translate_target']
        expiration, alternate, alternate_url = tw['expiration'], tw['alternate'], tw['alternate_url']     
        user, password = self.p.config['twitter_screen_name'], self.p.config['twitter_password']
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
        # sort out: url and text
        pattern = r'http[s]*\S+'
        urls = re.findall(pattern, tweets_to_store[0]['full_text'])
        full_text = re.sub(pattern, '', tweets_to_store[0]['full_text'])
        # translation
        if translate == 'True':
            _b = GoogleTranslator(source='auto', target='en').translate(full_text)
            # Fix EncodeError
            en = python_encoding(encoding)
            b = _b.encode(en, 'ignore').decode(en)
        else:
            b = full_text
        # keywords
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
        # time validation
        c = int()
        d_object = datetime.strptime(tweets_to_store[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        epoch = int(d_object.timestamp()) + self.p.timezone_offset # UTC + timezone_offset
        if re.match(r'[0-9.]+m', expiration):
            c = re.sub(r'([0-9.]+)m', r'\1',expiration)
            _c = float(c) * 60
        elif re.match(r'[0-9.]+h', expiration):
            c = re.sub(r'([0-9.]+)h', r'\1',expiration)
            _c = float(c) * 60 * 60

        if self.p.now - epoch <= _c and processing == True:
            processing = True
        elif self.p.now - epoch > _c and processing == True:
            processing = False
            
        if processing == True:
            if self.p.config['landscape'] == True:
                if not caption == str() and not a == None:
                    a += SVGtools.text('middle', '35', 95, (y + 35), caption).svg()
                disc = split_text(wordwrap=38, text=b, max_rows=5)
                for w in disc:
                    w = fix_text(w)
                    a += SVGtools.text('start', '30', 180, (y + 30), w).svg()
                    y += 38
            else:
                if not caption == str() and not a == None:
                    a += SVGtools.text('middle', '25', 95, (y + 55), caption).svg()
                disc = split_text(wordwrap=36, text=b, max_rows=8)
                for w in disc:
                    w = fix_text(w)
                    a += SVGtools.text('start', '20', 180, (y + 50), w).svg()
                    y += 25
            if len(urls) > 0:
                url = urls[0]
            else:
                url = alternate_url 
        else:
            a, url = None, None
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg(), url, processing
        
    def qrcode(self, url):
        import qrcode
        img = qrcode.make(url)
        png_qr = io.BytesIO()
        img.save(png_qr)
        return png_qr.getvalue()

class GraphLabel:
    def __init__(self, p, y, s):
        self.p = p
        self.y = y 
        self.s = s
        self.label = p.config['graph_labels'][s]
        self.canvas = p.config['graph_canvas']
        self.w =  self.canvas['width']
        self.h = self.canvas['height']
        self.bgcolor = self.canvas['bgcolor']
        self.axis = self.canvas['axis']
        self.axis_color = self.canvas['axis_color']
        self.grid = self.canvas['grid']
        self.grid_color = self.canvas['grid_color']
        self.start = self.label['start']
        self.end = self.label['end']
        self.step = self.label['step']
        self.basis = self.label['basis']
        self.font_size = self.label['font-size']

    def text(self):
        a = str()
        if re.match('hourly', self.s):    
            a += GraphLabel.hourly(self)
        elif re.match('daily', self.s):    
            a += GraphLabel.daily(self)
        return a + '\n'
        
    def hourly(self):
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / (self.end - self.start)
        a = str()
        d = read_i18n(self.p)
        c = 0
        for n in range(self.start, self.end, self.step):
            weather = self.p.HourlyForecast(n)
            heure = datetime.fromtimestamp(weather['dt'], self.p.config['tz']).strftime('%H')
            _x = int(sp_x + box_size_x * n + box_size_x * 0.5)
            if c % 3 == 1:
                heure = re.sub('^0', '', heure)
                a += SVGtools.text('middle', self.font_size, _x, (self.y + 4), str(heure)).svg()
            c += 1
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()
            
    def daily(self):
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / (self.end - self.start)
        a = str()
        d = read_i18n(self.p)
        for n in range(self.start, self.end, self.step):
            weather = self.p.DailyForecast(n)
            jour = str.lower(datetime.fromtimestamp(weather['dt'], self.p.config['tz']).strftime('%a'))
            jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
            _x = int(sp_x + box_size_x * (n - self.start) + box_size_x * 0.5)
            a += SVGtools.text('middle', self.font_size, _x, (self.y + 4), str(jour)).svg()
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()
 
class GraphLine:
    def __init__(self, p, y, obj):
        self.p = p
        self.y = y
        self.obj = obj
        self.start = self.obj['start']
        self.end = self.obj['end']
        self.stroke_color = self.obj['stroke-color']
        self.stroke_linecap = self.obj['stroke-linecap']
        self.stroke_width = self.obj['stroke-width']
        
    def draw(self): 
        style = f'stroke:{self.stroke_color};stroke-linecap:{self.stroke_linecap};stroke-width:{self.stroke_width}px;'
        i = SVGtools.line(x1=int(self.start), x2=int(self.end), y1=self.y, y2=self.y , style=style).svg()
        return i
        
class GraphPane:
    def __init__(self, p, y, obj):
        self.p = p
        self.y = y
        self.obj = obj
        self.type = self.obj['type']
        self.stroke = self.obj['stroke']
        self.stroke_color = self.obj['stroke-color']
        self.fill = self.obj['fill']
        self.stroke_linecap = self.obj['stroke-linecap']
        self.width = self.obj['width'] if 'width' in self.obj else None
        self.start = self.obj['start']
        self.end = self.obj['end']
        self.step = self.obj['step']
        self.basis = self.obj['basis']
        self.title = self.obj['title']
        self.canvas = p.config['graph_canvas']
        self.w =  self.canvas['width']
        self.h = self.canvas['height']
        self.bgcolor = self.canvas['bgcolor']
        self.axis = self.canvas['axis']
        self.axis_color = self.canvas['axis_color']
        self.grid = self.canvas['grid']
        self.grid_color = self.canvas['grid_color']
        self.grid_ext_upper = self.canvas['grid_ext_upper']
        self.grid_ext_lower= self.canvas['grid_ext_lower']
        self.style_bg = f'fill:{self.bgcolor};stroke:{self.bgcolor};stroke-width:0px;'
        self.style_axis = f'stroke:{self.axis_color};stroke-linecap:{self.stroke_linecap};stroke-width:1px;'
        self.style_grid = f'stroke:{self.grid_color};stroke-linecap:{self.stroke_linecap};stroke-width:{self.grid}px;'
        self.style_pline_fill = f'fill:{self.fill};stroke:{self.fill};stroke-width:0px;stroke-linecap:{self.stroke_linecap};'
        self.style_pline = f'fill:none;stroke:{self.stroke_color};stroke-width:{self.stroke}px;stroke-linecap:{self.stroke_linecap};'
        self.style_line = f'stroke:{self.stroke_color};stroke-linecap:{self.stroke_linecap};stroke-width:{self.stroke}px;'
        self.style_rect = f'fill:{self.fill};stroke:{self.stroke_color};stroke-linecap:{self.stroke_linecap};stroke-width:{self.stroke}px;'
        self.style_baseline = f'stroke:{self.axis_color};stroke-width:1px;'

    def draw(self):
        if self.type == 'line':
            a = self.line()
        elif self.type == 'spline':
            a = self.spline()
        elif self.type == 'bar':
            a = self.bar()
        elif self.type == 'rect':
            a = self.rect()
        elif self.type == 'tile':
            a = self.tile()
        return a

    def line(self):
        y = self.y
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / self.end
        half = box_size_x * 0.5
        a = str()
        d = read_i18n(self.p)
        tz = self.p.config['tz']       
        # draw canvas
        a += SVGtools.rect(x=sp_x, y=(y - self.h + 140), width=self.w, height=(self.h - 45), style=self.style_bg).svg()
        # get graph data
        points = str()
        if self.basis == 'hour':
            tMin = min([self.p.HourlyForecast(n)['temp'] for n in range(self.start, self.end, self.step)])
            tMax = max([self.p.HourlyForecast(n)['temp'] for n in range(self.start, self.end, self.step)])
            if self.p.config['landscape'] == True:
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                title = self.title + ', 24 hours'
                a += SVGtools.text('start', '16', 5, (self.p.config['h'] - 5), title).svg()
                c = 0
                for n in range(self.start, self.end, self.step):
                    weather = self.p.HourlyForecast(n)
                    x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp'] - tMin) * tStep + 75
                    points += f'{x},{_y} '
                    points2 = points + f'{x},{y + 95} {sp_x + half},{y + 95}'
                    if c % 3 == 0:    
                        a += SVGtools.text('middle', '25', x, (_y - 14), int(round(weather['temp']))).svg()
                        a += SVGtools.circle((x + 17), (_y - 29), 3, 'black', 2, 'none').svg()  
                    c += 1
            else:
                tStep = 35 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                title = self.title + ', 24 hours'
                a += SVGtools.text('start', '16', sp_x+5, (y - self.h + 156), title).svg()
                c = 0
                for n in range(self.start, self.end, self.step):
                    weather = self.p.HourlyForecast(n)
                    x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp'] - tMin) * tStep + 80
                    points += f'{x},{_y} '
                    points2 = points + f'{x},{(y + 95)} {int(sp_x + half)},{y + 95}'
                    if c % 3 == 0:    
                        a += SVGtools.text('middle', '16', x, (_y - 9), int(round(weather['temp']))).svg()
                        a += SVGtools.circle((x + 10), (_y - 20), 2, 'black', 1, 'none').svg()  
                    c += 1
        elif self.basis == 'day':
            tMin = min([self.p.DailyForecast(n)['temp_day'] for n in range(self.start, self.end, self.step)])
            tMax = max([self.p.DailyForecast(n)['temp_day'] for n in range(self.start, self.end, self.step)])
            if self.p.config['landscape'] == True:
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                title = f'{self.title}, {self.end} days'
                a += SVGtools.text('start', '16', 5, (self.p.config['h'] - 5), title).svg()
                for n in range(self.start, self.end, self.step):
                    weather = self.p.DailyForecast(n)
                    jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                    jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
                    x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep + 75
                    points += f'{x},{_y} '
                    points2 = points + f'{x},{y + 95} {int(sp_x + half)},{y + 95}'
                    a += SVGtools.text('middle', '25', x, (_y - 14), int(weather['temp_day'])).svg()
                    a += SVGtools.circle((x + 17), (_y - 29), 3, 'black', 2, 'none').svg()       
            else:
                tStep = 35 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                title = f'{self.title}, {self.end} days'
                a += SVGtools.text('start', '16', sp_x+5, (y - self.h + 156), title).svg()
                for n in range(self.start, self.end, self.step):
                    weather = self.p.DailyForecast(n)
                    jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                    jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
                    x = int(sp_x + box_size_x * n + half)
                    _y = y - (weather['temp_day'] - tMin) * tStep + 80
                    points += f'{x},{_y} '
                    points2 = points + f'{x},{y + 95} {int(sp_x + half)},{y + 95}'
                    a += SVGtools.text('middle', '16', x, (_y - 9), int(weather['temp_day'])).svg()
                    a += SVGtools.circle((x + 12), (_y - 20), 2, 'black', 1, 'none').svg() 
        # draw fill pline        
        a += SVGtools.polyline(points2, self.style_pline_fill).svg()
        # draw pline
        a += SVGtools.polyline(points, self.style_pline).svg()
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()
        
    def spline(self):
        y = self.y
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / self.end
        half_box = box_size_x * 0.5
        a = str()
        d = read_i18n(self.p)
        tz = self.p.config['tz']       
        # draw canvas
        a += SVGtools.rect(x=sp_x, y=(y - self.h + 140), width=self.w, height=(self.h - 45), style=self.style_bg).svg()
        # draw graph
        points = str()
        # get hourly temp graph data
        if self.basis == 'hour':
            # get max and min temp
            tMin = min([self.p.HourlyForecast(n)['temp'] for n in range(self.start, self.end, self.step)])
            tMax = max([self.p.HourlyForecast(n)['temp'] for n in range(self.start, self.end, self.step)])
            if self.p.config['landscape'] == True:
                # get graph y-axis step
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                # title
                title = self.title + ', 24 hours'
                a += SVGtools.text('start', '16', 5, (self.p.config['h'] - 5), title).svg()
                # computes temp x and y positions
                c = 0
                lst = list()
                for n in range(self.start, self.end, self.step):
                    weather = self.p.HourlyForecast(n)
                    x = int(sp_x + box_size_x * n + half_box)
                    _y = y - (weather['temp'] - tMin) * tStep + 75
                    lst.append((x, _y))
                    # add temp every 3 steps
                    if c % 3 == 0:    
                        a += SVGtools.text('middle', '25', x, (_y - 14), int(round(weather['temp']))).svg()
                        a += SVGtools.circle((x + 17), (_y - 29), 3, 'black', 2, 'none').svg()  
                    c += 1
        # get daily temp graph data
        elif self.basis == 'day':
            # get max and min temp
            tMin = min([self.p.DailyForecast(n)['temp_day'] for n in range(self.start, self.end, self.step)])
            tMax = max([self.p.DailyForecast(n)['temp_day'] for n in range(self.start, self.end, self.step)])
            if self.p.config['landscape'] == True:
                # get graph y-axis step
                tStep = 80 / (tMax - tMin) if (tMax - tMin) != 0 else 1
                # title
                title = f'{self.title}, {self.end} days'
                a += SVGtools.text('start', '16', 5, (self.p.config['h'] - 5), title).svg()
                # computes temp x and y positions
                lst = list()
                for n in range(self.start, self.end, self.step):
                    weather = self.p.DailyForecast(n)
                    jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                    jour = d['abbreviated_weekday'][jour] if not d == dict() else jour
                    x = int(sp_x + box_size_x * n + half_box)
                    _y = y - (weather['temp_day'] - tMin) * tStep + 75
                    lst.append((x, _y))
                    # add temp
                    a += SVGtools.text('middle', '25', x, (_y - 14), int(weather['temp_day'])).svg()
                    a += SVGtools.circle((x + 17), (_y - 29), 3, 'black', 2, 'none').svg()              
        # draw filled graph
        a += SVGtools.spline(lst=lst, _x=lst[0][0], _y=(y + 95), stroke=self.fill, stroke_width=0, fill=self.fill).svg()
        # draw spline graph
        a += SVGtools.spline(lst=lst, stroke=self.stroke_color, stroke_width=self.stroke).svg()
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()

    def bar(self):
        y = self.y
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / self.end
        a = str()
        i18n = read_i18n(self.p)
        # Canvas
        a += SVGtools.rect(x=sp_x, y=(y - self.h + 140), width=self.w, height=(self.h - 45), style=self.style_bg).svg()
        if self.basis == 'hour' and self.title == 'rain precipitation':
            # Graph
            th = 10.0 # threshold
            _min = min([self.p.HourlyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)])
            _max = max([self.p.HourlyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)])
            _sum = round(sum([self.p.HourlyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)]), 2)
            title = f'{self.title}, 24 hours'
            a += SVGtools.text('start', '16', sp_x+5, (y - self.h + 156), f'{title}, total: {int(round(_sum, 0))} mm').svg()
            for n in range(self.start, self.end, self.step):
                weather = self.p.HourlyForecast(n)
                vol = weather['rainAccumulation']
                base_y = y - self.h + 235
                _vol = int((vol **(1/3)) * th)
                x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.line(x1=x, x2=x, y1=base_y, y2=(base_y - _vol) , style=self.style_line).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16', x, (base_y - _vol - 10), f'{int(round(vol, 0))} mm').svg()
                    a += SVGtools.line(x, x, (base_y - _vol), (base_y - _vol - 8), self.style_axis).svg()
        elif self.basis == 'day' and self.title == 'rain precipitation':
            # Graph
            th = 5.75 # threshold
            _min = min([self.p.DailyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)])
            _max = max([self.p.DailyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)])
            _sum = round(sum([self.p.DailyForecast(n)['rainAccumulation'] for n in range(0, self.end, self.step)]), 2)
            title = f'{self.title}, {self.end} days'
            a += SVGtools.text('start', '16', sp_x+5, (y - self.h + 156), f'{self.title}, total: {int(round(_sum, 0))} mm').svg()
            for n in range(self.start, self.end, self.step):
                weather = self.p.DailyForecast(n)
                vol = weather['rainAccumulation']
                base_y = y - self.h + 235
                _vol = int((vol **(1/3)) * th)
                x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.line(x1=x, x2=x, y1=base_y, y2=(base_y - _vol) , style=self.style_line).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16', x, (base_y - _vol - 12), f'{int(round(vol, 0))} mm').svg()
                    a += SVGtools.line(x, x, (base_y - _vol), (base_y - _vol - 10), self.style_axis).svg()
        # Baseline
        a += SVGtools.line(x1=sp_x, x2=(sp_x + self.w), y1=(y + 95), y2=(y + 95), style=self.style_baseline).svg()
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()

    def rect(self):
        y = self.y
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        box_size_x = self.w / self.end
        a = str()
        i18n = read_i18n(self.p)
        # Canvas
        a += SVGtools.rect(x=sp_x, y=(y - self.h + 140), width=self.w, height=(self.h - 45), style=self.style_bg).svg() 
        if self.basis == 'hour' and self.title == 'snow accumulation':
            # Graph
            th = 10.0 # threshold 
            _min = min([self.p.HourlyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)])
            _max = max([self.p.HourlyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)])
            _sum = round(sum([self.p.HourlyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)]), 2)
            title = f'{self.title}, 24hours'
            for n in range(self.start, self.end, self.step):
                weather = self.p.HourlyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - self.h + 235
                _vol = int(vol **(1/3) * th)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.rect(x=_x - int(self.width / 2), y=(base_y - _vol), width=self.width , height=_vol , style=self.style_rect).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16', _x, (base_y - _vol - 12), f'{int(round(vol, 0))} mm').svg()
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), self.style_axis).svg()

        elif self.basis == 'day' and self.title == 'snow accumulation':
            # Graph
            th = 5.75 # threshold  
            _min = min([self.p.DailyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)])
            _max = max([self.p.DailyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)])
            _sum = round(sum([self.p.DailyForecast(n)['snowAccumulation'] for n in range(0, self.end, self.step)]), 2) 
            title = f'{self.title}, {self.end} days'
            for n in range(0, self.end, self.step):
                weather = self.p.DailyForecast(n)
                vol = weather['snowAccumulation']
                base_y = y - self.h + 235
                _vol = int(vol **(1/3) * th)
                _x = sp_x + int(box_size_x * n + box_size_x * 0.5)
                a += SVGtools.rect(x=_x - int(self.width / 2), y=(base_y - _vol), width=self.width , height=_vol , style=self.style_rect).svg()
                if _max == vol and _max != 0:
                    a += SVGtools.text('middle', '16', _x, (base_y - _vol - 12), f'{int(round(vol, 0))} mm').svg()
                    a += SVGtools.line(_x, _x, (base_y - _vol), (base_y - _vol - 10), self.style_axis).svg()
        # Baseline
        a += SVGtools.line(x1=(sp_x), x2=(sp_x + self.w), y1=(y + 95), y2=(y + 95), style=self.style_baseline).svg()
        # Text processing
        a += SVGtools.text('start', '16', sp_x+5, (y - self.h + 156), f'{title}, total: {int(round(_sum, 0))} mm').svg()
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()

    def tile(self):
        tz = self.p.config['tz']
        sp_x = int((self.p.config['w'] - self.w) * 0.5)
        kwargs = {  'p': self.p, 'y': self.y, 'w': self.w, 'h': self.h, 'bgcolor': self.bgcolor, 'axis': self.axis, 
                    'axis_color': self.axis_color, 'grid': self.grid, 'grid_color': self.grid_color, 
                    'grid_ext_upper': self.grid_ext_upper, 'grid_ext_lower': self.grid_ext_lower, 
                    'title': self.title, 'start': self.start, 'step': self.step, 'end': self.end, 
                    'basis': self.basis, 'stroke': self.stroke, 
                    'stroke_color': self.stroke_color, 'fill': self.fill, 'stroke_linecap': self.stroke_linecap, 
                    'tz': tz, 'sp_x': sp_x}
        # Start
        a = str()
        # Canvas 
        a += SVGtools.rect(x=sp_x, y=(self.y - self.h + 140), width=self.w, height=(self.h - 45), style=self.style_bg).svg()

        def daily_weather(p, y, w, h, bgcolor, axis, axis_color, grid, grid_color, grid_ext_upper, grid_ext_lower, \
                            stroke, stroke_color, fill, stroke_linecap, \
                            title, start, end, step, basis, tz, sp_x, **kwargs):
            box_size_x = (w - (end - start - 1) * grid) / (end - start)
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p)
            i, s = str(), str()
            for n in range(start, end, step):
                weather = p.DailyForecast(n)
                jour = str.lower(datetime.fromtimestamp(weather['dt'], tz).strftime('%a'))
                #jour = i18n["abbreviated_weekday"][jour] if not i18n == dict() else jour
                # tweak weather icon
                dt = weather['dt']
                sunrise = weather['sunrise']
                sunset = weather['sunset']
                state = daytime(p=p, dt=dt, sunrise=sunrise, sunset=sunset)
                if state == 'polar_night' and re.search('Day', weather['main']):
                    weather['main'] = re.sub('Day', 'Night', weather['main'])
                elif state == 'midnight_sun' and re.search('Night', weather['main']):
                    weather['main'] = re.sub('Night', 'Day', weather['main'])
                _x = int(sp_x + (box_size_x + grid) * (n - start))
                _y = y + 90
                if p.config['landscape'] == True:
                    i += SVGtools.transform(f'(1.8,0,0,1.8,{(_x - 10)},{(_y - 180)})', addIcon(weather['main'])).svg()
                    s += SVGtools.text(anchor='end', fontsize='30', x=(_x + half - 20), y=_y, v=round(weather['temp_min']), stroke='rgb(128,128,128)').svg()
                    s += SVGtools.circle((_x + half - 14), (_y - 20), 3, 'rgb(128,128,128)', 2, 'none').svg()
                    s += SVGtools.text('end', '30', (_x + half + 45), _y, round(weather['temp_max'])).svg()
                    s += SVGtools.circle((_x + half + 51), (_y - 20), 3, 'black', 2, 'none').svg()
                    if n < (end - 1):
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55 - grid_ext_upper), (_y + 5), self.style_grid).svg()
                else:
                    sp = 0 if (end - start) == 6 else -10
                    i += SVGtools.transform(f'(1.0,0,0,1.0,{(_x - 10 + sp)},{(_y - 100)})', addIcon(weather['main'])).svg()
                    s += SVGtools.text('end', '16', (_x + half), _y, '/').svg()
                    s += SVGtools.text('end', '16', (_x + half - 8), _y, round(weather['temp_min'])).svg()
                    s += SVGtools.circle((_x + half - 6), (_y - 10), 2, 'black', 1, 'none').svg()
                    s += SVGtools.text('end', '16', (_x + half + 22), _y, round(weather['temp_max'])).svg()
                    s += SVGtools.circle((_x + half + 24), (_y - 10), 2, 'black', 1, 'none').svg()
                    #if n < (end - 1):
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 55-10), (_y + 10), self.style_grid).svg()
            return s,i

        def moon_phase(p, y, w, h, bgcolor, axis, axis_color, grid, grid_color, stroke, stroke_color, fill, stroke_linecap, \
                             grid_ext_upper, grid_ext_lower, title, start, end, step, basis, tz, sp_x, **kwargs):
            box_size_x = (w - (end - start - 1) * grid) / (end - start)
            half = int(box_size_x * 0.5)
            i18n = read_i18n(p)
            ramadhan = p.config['ramadhan']
            i, s = str(),str()
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
                        i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 150 - grid_ext_upper), (_y + 105), self.style_grid).svg()                 
                    # Moon icon
                    r = 25
                    kw = {'p': p, 'day': day, 'mon': mon, 'yr': yr, 'lat': lat, 'rx': _x + half, 'ry': _y + 7, 'r': r, 'ramadhan': ramadhan}
                    m = Moonphase(**kw)
                    dm, ps, ram = m.calc()
                    style = f'fill:{fill};stroke:{stroke_color};stroke-width:1px;'
                    i += m.svg(dm=dm, ps=ps, stroke_color=stroke_color, r_plus=2, stroke=stroke, style=style)
                    # Text: moonrise and moonset
                    s += SVGtools.text('middle', '25', (_x + half), (_y + 80), moonrise).svg()
                    s += SVGtools.text(anchor='middle', fontsize='25', x=(_x + half), y=(_y + 103), v=moonset, stroke='rgb(128,128,128)').svg()
                    # Text: moon phase and ramadhan
                    d = {'n': 'new', '1': 'first', 'f': 'full', '3': 'last'}
                    ps = d[ps] if ps in d else str()
                    ram = 'ram' if ram == 'r' else str()
                    cap = ','.join(x for x in [ps, ram] if not x == str())
                    s += SVGtools.text2('middle', 'bold', '18', (_x + half), (_y + 55), cap).svg()
                else:
                    _x = int(sp_x + (box_size_x + grid) * (n - start)) 
                    _y = y + 25  
                    r = 18 if end == 6 else 14
                    i += SVGtools.line((_x + box_size_x), (_x + box_size_x), (_y - h + 115), (_y + 70), self.style_grid).svg()                 
                    # Moon icon
                    kw = {'p': p, 'day': day, 'mon': mon, 'yr': yr, 'lat': lat, 'rx': _x + half, 'ry': _y + 7, 'r': r, 'ramadhan': ramadhan}
                    m = Moonphase(**kw)
                    dm, ps, ram = m.calc()
                    style = f'fill:{fill};stroke:{stroke_color};stroke-width:1px;'
                    i += m.svg(dm=dm, ps=ps, stroke_color=stroke_color, r_plus=2, stroke=stroke, style=style)
                    # Text: moonrise and moonset
                    s += SVGtools.text('middle', '16', (_x + int(box_size_x * 0.5)), (_y + 50), moonrise).svg()
                    s += SVGtools.text('middle', '16', (_x + int(box_size_x * 0.5)), (_y + 68), moonset).svg()
                    style = 'stroke:black;stroke-width:1px;'
                    i += SVGtools.line((_x + half - 25), (_x  + half + 25), (_y + 54), (_y + 54), style).svg()
                    # Text: moon phase and ramadhan 
                    s += SVGtools.text('start', '16', (_x + 3), (_y - 8), f'{ps}').svg()
                    s += SVGtools.text('end', '16', (_x + box_size_x - 3), (_y - 8), f'{ram}').svg()      
            return s,i
        # Graph
        if self.basis == 'day' and self.title == 'weather':
            s,i = daily_weather(**kwargs)
            a += s + i
        elif self.basis == 'day' and self.title == 'moon phase':
            s,i = moon_phase(**kwargs)        
            if self.p.config['landscape'] == True:
                s += SVGtools.text('start', '16', 10, (self.p.config['h'] - 5), 'moon phase').svg()
            a += s + i         
        return SVGtools.fontfamily(font=self.p.config['font'], _svg=a).svg()
 
class Moonphase:
    def __init__(self, **kw):
        self.p = kw.get('p')
        self.day = kw.get('day')
        self.mon = kw.get('mon')
        self.yr = kw.get('yr')
        self.lat = kw.get('lat')
        self.rx = kw.get('rx')
        self.ry = kw.get('ry')
        self.r = kw.get('r')
        self.ramadhan = kw.get('ramadhan')
        weather = self.p.CurrentWeather()
        self.darkmode = dark_mode(self.p, self.p.now, weather['sunrise'], weather['sunset'])
        
    def svg(self, dm, ps, stroke_color, r_plus, stroke, style):
        s = SVGtools.circle(self.rx, self.ry, (self.r + 2), stroke_color, stroke, "none").svg()
        s += SVGtools.path(dm, style).svg() if ps != 'f' else ''
        return s
        
    def calc(self):
        from hijridate import Hijri, Gregorian
        from astral import moon
        
        def phase(rad):
            if self.p.config['cloudconvert'] == True:
                one_day_step = 2 * pi / 56
            else:
                one_day_step = abs(2 * pi / 56)  # cairo fix
                
            if one_day_step > rad >= 0 or one_day_step > (pi * 2 - rad) >= 0:
                a = 'n'
            elif one_day_step > abs(rad - pi * 0.5) >= 0:
                a = '1'
            elif one_day_step > abs(rad - pi) >= 0:
                a = 'f'
            elif one_day_step > abs(rad - pi * 1.5) >= 0:
                a = '3'
            else:
                a = str()
            return a

        def moonphase(day, mon, yr):
            #g = Gregorian(yr, mon, day).to_hijri()
            #_, _, d = g.datetuple()
            #mooncycle = 29.55
            mooncycle = 27.99
            #a = d / mooncycle
            a = moon.phase(date(yr, mon, day)) / mooncycle
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
        # cairosvg bug?
        pi = math.pi
        if self.darkmode == True:
            pi = pi
            self.lat = -self.lat
            
        if not self.p.config['cloudconvert'] == True: 
            pi = -pi

        #rad = weather['moon_phase'] * pi * 2  
        # One call API: 0 or 1:new moon, 0.25:first qurater moon, 0.5:full moon, 0.75:third quarter moon 
        val = moonphase(self.day, self.mon, self.yr) # Astral v3.0 module
        rad = val * pi * 2 if val < 1 else pi * 2  
        c = 0.025
        m = rad * c * math.cos(rad)
        rp = self.r + 2      # diameter r
        ra1 = 1 * rp
        ra2 = (math.cos(rad) * rp)
        ra3 = 1 * rp
        if self.lat >= 0:
            if phase(rad) == 'n':  # new moon
                px1 = math.cos(pi * 0.5 - m) * rp + self.rx
                py1 = math.sin(pi * 0.5 - m) * rp + self.ry
                px2 = math.cos(pi * 0.5 - m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 - m) * rp + self.ry
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 1 {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif rad < pi * 0.5:  # new moon to first quarter
                px1 = math.cos(pi * 0.5 - m) * rp + self.rx
                py1 = math.sin(pi * 0.5 - m) * rp + self.ry
                px2 = math.cos(pi * 0.5 - m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 - m) * rp + self.ry
                flag = 0 if self.darkmode == True else 1
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif pi > rad >= pi * 0.5:  # first quarter to full moon
                px1 = math.cos(pi * 0.5 + m) * rp + self.rx
                py1 = math.sin(pi * 0.5 + m) * rp + self.ry
                px2 = math.cos(pi * 0.5 + m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 + m) * rp + self.ry
                flag = 1 if self.darkmode == True else 0
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif pi * 1.5 > rad >= pi:  # full moon to third quarter
                px1 = math.cos(pi * 1.5 + m) * rp + self.rx
                py1 = math.sin(pi * 1.5 + m) * rp + self.ry
                px2 = math.cos(pi * 1.5 + m) * rp + self.rx
                py2 = -math.sin(pi * 1.5 + m) * rp + self.ry
                flag = 1 if self.darkmode == True else 0
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            else:  # third quarter to new moon
                px1 = math.cos(pi * 1.5 - m) * rp + self.rx
                py1 = math.sin(pi * 1.5 - m) * rp + self.ry
                px2 = math.cos(pi * 1.5 - m) * rp + self.rx
                py2 = -math.sin(pi * 1.5 - m) * rp + self.ry
                flag = 0 if self.darkmode == True else 1
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
        else:
            if phase(rad) == 'n':
                px1 = math.cos(pi * 0.5 + m) * rp + self.rx
                py1 = math.sin(pi * 0.5 + m) * rp + self.ry
                px2 = math.cos(pi * 0.5 + m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 + m) * rp + self.ry
                flag = 0 if self.darkmode == True else 1
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif rad < pi * 0.5:
                px1 = math.cos(pi * 1.5 - m) * rp + self.rx
                py1 = math.sin(pi * 1.5 - m) * rp + self.ry
                px2 = math.cos(pi * 1.5 - m) * rp + self.rx
                py2 = -math.sin(pi * 1.5 - m) * rp + self.ry
                flag = 0 if self.darkmode == True else 1
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif pi > rad >= pi * 0.5:
                px1 = math.cos(pi * 1.5 + m) * rp + rx
                py1 = math.sin(pi * 1.5 + m) * rp + ry
                px2 = math.cos(pi * 1.5 + m) * rp + rx
                py2 = -math.sin(pi * 1.5 + m) * rp + ry
                flag = 1 if self.darkmode == True else 0
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            elif pi * 1.5 > rad >= pi:
                px1 = math.cos(pi * 0.5 + m) * rp + self.rx
                py1 = math.sin(pi * 0.5 + m) * rp + self.ry
                px2 = math.cos(pi * 0.5 + m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 + m) * rp + self.ry
                flag = 1 if self.darkmode == True else 0
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
            else:
                px1 = math.cos(pi * 0.5 - m) * rp + self.rx
                py1 = math.sin(pi * 0.5 - m) * rp + self.ry
                px2 = math.cos(pi * 0.5 - m) * rp + self.rx
                py2 = -math.sin(pi * 0.5 - m) * rp + self.ry
                flag = 0 if self.darkmode == True else 1
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 1 1 {px2} {py2} {ra2} {ra3} 0 0 {flag} {px1} {py1}z'
                ps = phase(rad)
                ram = calc_ramadhan(self.day, self.mon, self.yr) if self.ramadhan == True else str()
        return dm, ps, ram

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

