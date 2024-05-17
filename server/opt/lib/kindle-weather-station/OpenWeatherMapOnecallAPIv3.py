#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Date       : 24 April 2024 

import time as t
import json
import requests
#import pytz
#from datetime import datetime,timedelta,timezone
from pytz import timezone
from datetime import datetime,timedelta

def readSettings(settings):
    OWM_config = './config/OWM_API_KEY.json'
    graph_config = './config/graph_config.json'
    twitter_config = './config/twitter_ID.json'
    a = dict()
    with open(settings, 'r') as f:
        service = json.load(f)['station']
        a['city'] = service['city'] if 'city' in service else None
        a['timezone'] = service['timezone'] if 'timezone' in service else None
        a['locale'] = service['locale'] if 'locale' in service else 'en_US.UTF-8'
        a['encoding'] = service['encoding'] if 'encoding' in service else 'iso-8859-1'
        a['font'] = service['font'] if 'font' in service else 'Droid Sans'
        a['sunrise_and_sunset'] = bool(eval(service['sunrise_and_sunset'])) if 'sunrise_and_sunset' in service else True
        a['darkmode'] = service['darkmode'] if 'darkmode' in service else 'False'
        a['api'] = service['api']
        a['lat'] = service['lat']
        a['lon'] = service['lon']
        a['units'] = service['units'] if 'units' in service else 'metric'
        a['lang'] = service['lang'] if 'lang' in service else 'en'
        a['in_clouds'] = service['in_clouds'] if 'in_clouds' in service else str()  # Options: "cloudCover", "probability"
        a['cloudconvert'] = bool(eval(service['cloudconvert'])) if 'cloudconvert' in service else False
        a['converter'] = service['converter'] if 'converter' in service else None
        a['layout'] = service['layout']
        a['ramadhan'] = bool(eval(service['ramadhan'])) if 'ramadhan' in service else False
        a['twitter'] = service['twitter'] if 'twitter' in service else False
        if 'twitter_keywords' in service:
            a['twitter_include_keywords'] = service['twitter_keywords']['include'] if 'include' in service['twitter_keywords'] else str()
            a['twitter_exclude_keywords'] = service['twitter_keywords']['exclude'] if 'exclude' in service['twitter_keywords'] else str()
        else:
             a['twitter_keywords'] = False
        c = service['graph_canvas'] if 'graph_canvas' in service else 'default'
        # Add timezone offset
        tz = timezone(a['timezone'])
        _tz = tz.utcoffset(datetime.now(), is_dst = True)
        offset = _tz.seconds if _tz.days == 0 else -_tz.seconds
        a['timezone_offset'] = offset
        
    try:
        b = list(reversed(service['graph_objects'])) if 'graph_objects' in service else None
        if not b == None:
            with open(graph_config, 'r') as f:
                graph = json.load(f)['graph']
                a['graph_canvas'] = graph['canvas'][service['graph_canvas']]
                a['graph_objects'] = list()
                a['graph_labels'] = graph['labels']
                for n in b:
                    a['graph_objects'].append(graph['objects'][n])
        else:
            a['graph_canvas'] = dict()
            a['graph_objects'] = list()
            a['graph_labels'] = dict()             
    except Exception as e:
        a['graph_canvas'] = dict()
        a['graph_objects'] = list()
        a['graph_labels'] = dict()

    try:
        with open(twitter_config, 'r') as f:
            t = json.load(f)['twitter']
            a['twitter_screen_name'] =  t["user_screen_name"]
            a['twitter_password'] =  t["password"]
    except Exception as e:
        a['twitter_screen_name'] = None
        a['twitter_password'] = None
    
    with open(OWM_config, 'r') as f:
        owm = json.load(f)['OWM']
        a['api_key'] = owm['api_key']
        a['service'] = owm['service']        
        a['api_version'] = owm['onecall_version']
        a['exclude'] = owm['exclude']  if 'exclude' in service else None
    return a

class OpenWeatherMap:
    icon = str()
    units = dict()
    direction = str()

    def __init__(self, settings, api_data=None):
        s = str()
        self.now = int(t.time())
        self.config = readSettings(settings)
        self.api_data = api_data
        self.timezone_offset = self.config['timezone_offset']
        if self.config['units'] == 'metric':
            self.units = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'C'}
        elif self.config['units'] == 'imperial':
            self.units = {'pressure': 'hPa', 'wind_speed': 'mph', 'temp': 'F'}
        else:
            self.units = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'K'}
        

    def ApiCall(self):
        s = str()
        now = self.now
        config = self.config
        s += 'lat=' + config['lat'] + '&lon=' + config['lon']
        s += '&units=' + config['units'] if 'units' in config and not config['units'] == None else ''
        s += '&lang=' + config['lang'] if 'lang' in config and not config['lang'] == None else ''
        s += ('&exclude=' + config['exclude'] if 'exclude' in config and not config['exclude'] == None else '')
        s += '&appid=' + config['api_key']
        url = 'https://api.openweathermap.org/data/' + config['api_version'] + '/onecall?' + s
        api_data = requests.get(url).json()            
        # sanity check
        if 'cod' in api_data and api_data['cod'] == 401:
            print('OpenWeatherMap: Invalid API Key, requests call rejected.')
            exit(1)         
        return api_data    

    def CurrentWeather(self):
        config = self.config
        c = self.api_data['current']
        h = self.api_data['hourly'][0]
        if not 'sunrise' in c:
            c['sunrise'] = None
        if not 'sunset' in c:
            c['sunset'] = None
        # Add hourly precipitation of rain or snow
        if 'rain' in h:
            c['rainAccumulation'] = float(h['rain']['1h'])
        else:
            c['rainAccumulation'] = 0
        if 'snow' in h:
            c['snowAccumulation'] = float(h['snow']['1h'])
        else:
            c['snowAccumulation'] = 0
        # Add 'in_clouds'
        c['cloudCover'] = c['clouds']
        #c['pop'] = round(c['cloudCover'] / 100,1)
        if config['in_clouds'] == 'cloudCover':
            c['in_clouds'] = round(c['cloudCover'] / 100,1)
        elif config['in_clouds'] == 'probability':
            c['in_clouds'] = round(c['pop'],1) if 'pop' in c else 0
        else:
            c['in_clouds'] = 0   
        # Add cardinal direction
        c['cardinal'] = self.cardinal(c['wind_deg'])
        # Get simplicity
        c['id'] = int(c['weather'][0]['id'])
        c['main'] = str(c['weather'][0]['main'])
        c['description'] = str(c['weather'][0]['description'])
        c['icon'] = str(c['weather'][0]['icon'])
        c['main'] = self.fixIcon(c)
        c['main'] = self.rename_weather(c['main'])
        return c

    def HourlyForecast(self, hour):
        config = self.config
        h = self.api_data['hourly'][hour]
        wind_gust = float(h['wind_gust']) if 'wind_gust' in h else None
        wind_deg = float(h['wind_deg']) if 'wind_deg' in h else None
        # Add hourly precipitation of rain or snow
        if 'rain' in h:
            h['rainAccumulation'] = float(h['rain']['1h'])
        else:
            h['rainAccumulation'] = 0
        if 'snow' in h:
            h['snowAccumulation'] = float(h['snow']['1h'])
        else:
            h['snowAccumulation'] = 0
        # Add 'in_clouds'
        h['cloudCover'] = h['clouds']
        if config['in_clouds'] == 'cloudCover':
            h['in_clouds'] = round(h['cloudCover'] / 100,1)
        elif config['in_clouds'] == 'probability':
            h['in_clouds'] = round(h['pop'],1) if 'pop' in h else 0
        else:
            h['in_clouds'] = 0
        # Add cardinal direction
        h['cardinal'] = self.cardinal(h['wind_deg'])
        # Get simplicity
        h['id'] = int(h['weather'][0]['id'])
        h['main'] = str(h['weather'][0]['main'])
        h['description'] = str(h['weather'][0]['description'])
        h['icon'] = str(h['weather'][0]['icon'])
        h['main'] = self.fixIcon(h)
        h['main'] = self.rename_weather(h['main'])
        return h

    def DailyForecast(self, day):
        config = self.config
        d = self.api_data['daily'][day]
        wind_gust = float(d['wind_gust']) if 'wind_gust' in d else None
        wind_deg = float(d['wind_deg']) if 'wind_deg' in d else None
        # Add hourly precipitation of rain or snow
        if 'rain' in d:
            d['rainAccumulation'] = float(d['rain'])
        else:
            d['rainAccumulation'] = 0
        if 'snow' in d:
            d['snowAccumulation'] = float(d['snow'])
        else:
            d['snowAccumulation'] = 0
        # Add 'in_clouds'
        d['cloudCover'] = d['clouds']
        if config['in_clouds'] == 'cloudCover':
            d['in_clouds'] = round(d['cloudCover'] / 100,1)
        elif config['in_clouds'] == 'probability':
            d['in_clouds'] = round(d['pop'],1) if 'pop' in d else 0
        else:
            d['in_clouds'] = 0 
        # Add wind gust
        d['wind_gust'] = wind_gust       
        # Add cardinal direction
        d['cardinal'] = self.cardinal(wind_deg)
        # Get simplicity
        d['id'] = int(d['weather'][0]['id'])
        d['main'] = str(d['weather'][0]['main'])
        d['description'] = str(d['weather'][0]['description'])
        d['icon'] = str(d['weather'][0]['icon'])
        d['temp_day'] = float(d['temp']['day'])
        d['temp_min'] = float(d['temp']['min'])
        d['temp_max'] = float(d['temp']['max'])
        d['temp_night'] = float(d['temp']['night'])
        d['temp_eve'] = float(d['temp']['eve'])
        d['temp_morn'] = float(d['temp']['morn'])
        d['main'] = self.fixIcon(d)       
        d['main'] = self.rename_weather(d['main'])
        return d

    def fixIcon(self, p):
        daytime = 'day' if p['icon'][-1] == 'd' else 'night'
        if p['main'] == 'Clear':
            a = p['main'] + '-' + daytime
        elif p['main'] == 'Clouds' and p['description'] == 'few clouds':
            a = 'Few-clouds' + '-' + daytime
        elif p['main'] == 'Snow' and (p['id'] == 611 or p['id'] == 612 or p['id'] == 613):
            a = 'Sleet'
        elif p['main'] == 'Snow' and (p['id'] == 602 or p['id'] == 622):
            a = 'Snow2'
        else:
            a = p['main']
        return a

    def rename_weather(self, s):
        d = {'Clear-day': 'ClearDay',
            'Clear-night': 'ClearNight',
            'Clouds': 'Cloudy',
            'Few-clouds': 'PartlyCloudy',
            'Few-clouds-day': 'PartlyCloudyDay',
            'Few-clouds-night': 'PartlyCloudyNight'
        } 
        a = d[s] if s in d else s
        return a

    def cardinal(self, degree):
        if degree >= 348.75 or degree <= 33.75: return 'N'
        elif 33.75 <= degree <= 78.75: return 'NE'
        elif 78.75 <= degree <= 123.75: return 'E'
        elif 123.75 <= degree <= 168.75: return 'SE'
        elif 168.75 <= degree <= 213.75: return 'S'
        elif 213.75 <= degree <= 258.75: return 'SW'
        elif 258.75 <= degree <= 303.75: return 'W'
        elif 303.75 <= degree <= 348.75: return 'NW'
        else: return None


# test
#print('current',OpenWeatherMap('settings.json').CurrentWeather(), '\n')
#print('hourly', OpenWeatherMap('settings.json').HourlyForecast(1), '\n')
#print('daily', OpenWeatherMap('settings.json').DailyForecast(1), '\n')