#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Date       : 24 April 2024 

import time as t
import json
import re
import requests
import zoneinfo
from datetime import datetime,timedelta

wether_codes_config = './config/tomorrow_codes.json'
    
def readSettings(setting):
    tomorrow_io_config = './config/tomorrow_io_API_KEY.json'
    graph_config = './config/graph_config.json'
    twitter_config = './config/twitter_ID.json'
    i18n_file = './config/i18n.json'
    
    with open(setting, 'r') as f:
        service = json.load(f)['station']
    f.close()
    
    a = dict()
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
    a['wind_icon'] = bool(eval(service['wind_icon'])) if 'wind_icon' in service else False
    a['cloudconvert'] = bool(eval(service['cloudconvert'])) if 'cloudconvert' in service else False
    a['layout'] = service['layout']
    a['system'] = service['system'] if 'system' in service else None
    a['landscape'] = bool(eval(service['landscape'])) if 'landscape' in service else False
    
    if a['landscape'] == True:
        a['w'], a['h'] = 800, 600
    else:
        a['w'], a['h']= 600, 800    
    
    a['ramadhan'] = bool(eval(service['ramadhan'])) if 'ramadhan' in service else False
    a['twitter'] = service['twitter'] if 'twitter' in service else False
    tz = zoneinfo.ZoneInfo(a['timezone'])
    _tz = tz.utcoffset(datetime.now())
    offset = _tz.seconds if _tz.days == 0 else -_tz.seconds
    a['timezone_offset'] = offset
    a['tz'] = tz
    a['UTC'] = zoneinfo.ZoneInfo('UTC')
    a['i18n_file'] = i18n_file
    
    with open(graph_config, 'r') as f:
        graph = json.load(f)['graph']
    f.close()
    
    a['graph_lines'] = graph['lines']
    a['graph_labels'] = graph['labels']
    b = list(reversed(service['graph_objects'])) if 'graph_objects' in service else None
    if not b == None:
        a['graph_canvas'] = graph['canvas'][service['graph_canvas']]
        a['graph_objects'] = list()
        for n in b:
            a['graph_objects'].append(graph['objects'][n])           
    else:
        a['graph_canvas'] = dict()
        a['graph_objects'] = list()

    if not a['twitter'] == False:
        with open(twitter_config, 'r') as f:
            tw = json.load(f)['twitter']
        f.close()
        a['twitter_screen_name'] =  tw["user_screen_name"]
        a['twitter_password'] =  tw["password"]
    
    with open(tomorrow_io_config, 'r') as f:
        c = json.load(f)['tomorrow.io']
    f.close()
    
    a['api_key'] = c['api_key']
    a['api_version'] = c['version']
    a['service'] = c['service']      
    #a['service_timesteps'] = ['1m', '1h', '1d']
    a['service_timesteps'] = ['1h', '1d']
    a['service_1m_rows'] = 6
    a['service_fields'] = { '1h': ['temperature', 'humidity', 'windSpeed', 'windDirection','pressureSeaLevel', \
                                    'weatherCode','precipitationProbability','cloudCover', 'rainAccumulation', 'snowAccumulation', \
                                    ],
                            '1d': ['temperature', 'humidity', 'windSpeed', 'windDirection','pressureSeaLevel', \
                                    'sunriseTime','sunsetTime','weatherCodeFullDay','weatherCode','precipitationProbability', \
                                    'cloudCover', 'moonriseTime', 'moonsetTime', 'temperatureMax', 'temperatureMin', \
                                    'rainAccumulation', 'snowAccumulation']
                            }
    #a['service_fields'] = {'1m': ['temperature', 'humidity', 'windSpeed', 'windDirection','pressureSeaLevel', \
    #                                'weatherCode','precipitationProbability','cloudCover'],
    #                        '1h': ['temperature', 'humidity', 'windSpeed', 'windDirection','pressureSeaLevel', \
    #                                'weatherCode','precipitationProbability','cloudCover', 'rainAccumulation', 'snowAccumulation'],
    #                        '1d': ['temperature', 'humidity', 'windSpeed', 'windDirection','pressureSeaLevel', \
    #                                'sunriseTime','sunsetTime','weatherCodeFullDay','weatherCode','precipitationProbability', \
    #                                'cloudCover', 'moonriseTime', 'moonsetTime', 'temperatureMax', 'temperatureMin', \
    #                                'rainAccumulation', 'snowAccumulation']
    #                        }
    return a

class TomorrowIo:
    icon = str()
    units = dict()
    direction = str()

    def __init__(self, setting, api_data=None):
        s = str()
        now = int(t.time())
        self.now = now
        self.config = readSettings(setting)
        self.api_data = api_data
        config = self.config
        self.timezone_offset = config['timezone_offset']
        location = config['lat'] + ',' + config['lon']
        fields = config['service_fields']
        url = "https://api.tomorrow.io/" + config['api_version'] + "/timelines"

        with open(wether_codes_config, 'r') as f:
            tomorrow_codes = json.load(f)
        self.tomorrow_codes = tomorrow_codes
       
        if self.config['units'] == 'metric':
            self.units = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'C'}
        elif self.config['units'] == 'imperial':
            self.units = {'pressure': 'inHg', 'wind_speed': 'mph', 'temp': 'F'}
        else:
            self.units = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'K'}

    def ApiCall(self):
        s = str()
        now = self.now
        config = self.config
        location = config['lat'] + ',' + config['lon']
        fields = config['service_fields']
        url = "https://api.tomorrow.io/" + config['api_version'] + "/timelines"
        api_data = dict()
        for n in config['service_timesteps']:
            if n == '1m':
                utc = config['UTC']
                #tz = timezone('utc')
                a = datetime.fromtimestamp(now, utc)
                yr, mon, day, hr, mi, _, _, _, _ = a.timetuple()
                b1 = int(mi)
                b2 = int(config['service_1m_rows'])
                endtime = f'{yr}-{mon}-{day}T{hr}:{b1}{b2}:00Z'
                querystring = {
                    'location': location,
                    'fields': fields[n],
                    'units': config['units'],
                    'timesteps': n,
                    'apikey': config['api_key'],
                    'timezone': config['timezone'],
                    'endtime': endtime}
            else:
                querystring = {
                    "location":location,
                    "fields":fields[n],
                    "units":config['units'],
                    "timesteps":n,
                    'timezone': config['timezone'],
                    "apikey":config['api_key']}
                    
            r = requests.request("GET", url, params=querystring)
            if  r.ok:
                api_data[n] = r.json()
                t.sleep(1)
            else:
                print('API: Requests call rejected.')
                exit(1)    
        return api_data

    def CurrentWeather(self):
        config = self.config
        #c = self.api_data['1m']['data']['timelines'][0]['intervals'][0]['values']
        c = self.api_data['1h']['data']['timelines'][0]['intervals'][0]['values']
        s = self.api_data['1h']['data']['timelines'][0]['intervals'][0]['startTime']
        d = self.api_data['1d']['data']['timelines'][0]['intervals'][0]['values']
        tomorrow_codes = self.tomorrow_codes
        
        # Time
        c['dt'] = self.conv_epoch(s)
        # Sunrise and Sunset
        c['sunrise'] = self.conv_epoch(d['sunriseTime']) if not d['sunriseTime'] == None else 0
        c['sunset'] = self.conv_epoch(d['sunsetTime']) if not d['sunsetTime'] == None else 0
        # daitime
        c['daytime'] = self.daytime(dt=c['dt'], sunrise=c['sunrise'], sunset=c['sunset'])
        # Temperature
        c['temp'] = float(c['temperature'])
        # Pressure
        c['pressure'] = float(c['pressureSeaLevel'])
        # Clouds
        c['clouds'] = float(c['cloudCover'])
        # Wind speed and Cardinal direction
        c['wind_speed'] = float(c['windSpeed'])
        c['cardinal'] = self.cardinal(float(c['windDirection']))
        # Weather disc
        code_fullday = str(d['weatherCodeFullDay']) # int() to str() data
        code_fullday = self.fix_weather(daytime=c['daytime'], code=code_fullday)
        c['description'] = tomorrow_codes['weatherCodeFullDay'][code_fullday]
        # Main weather
        code_day = str(c['weatherCode']) # int() to str() data
        code_day = self.fix_weather(daytime=c['daytime'], code=code_day) 
        w = tomorrow_codes["weatherCode"][code_day]    
        c['main'] = self.fix_kindle_weather(w)
        # Add pop
        c['pop'] = round(float(c['precipitationProbability']) / 100,1)
        # Add 'in_clouds'
        if config['in_clouds'] == 'cloudCover':
            c['in_clouds'] = round(float(c['cloudCover']) / 100,1)
        elif config['in_clouds'] == 'probability':
            c['in_clouds'] = round(c['pop'],1) if 'pop' in c else 0
        else:
            c['in_clouds'] = 0
        return c

    def HourlyForecast(self, hour):
        config = self.config
        h = self.api_data['1h']['data']['timelines'][0]['intervals'][hour]['values']
        s = self.api_data['1h']['data']['timelines'][0]['intervals'][hour]['startTime']
        d = self.api_data['1d']['data']['timelines'][0]['intervals'][0]['values']
        tomorrow_codes = self.tomorrow_codes       
        # Time
        h['dt'] = self.conv_epoch(s)
        # Sunrise and Sunset
        h['sunrise'] = self.conv_epoch(d['sunriseTime']) if not d['sunriseTime'] == None else 0
        h['sunset'] = self.conv_epoch(d['sunsetTime']) if not d['sunsetTime'] == None else 0
        # daitime
        h['daytime'] = self.daytime(dt=h['dt'], sunrise=h['sunrise'], sunset=h['sunset'])
        # Temperature
        h['temp'] = float(h['temperature'])
        # Pressure
        h['pressure'] = float(h['pressureSeaLevel'])
        # Clouds
        h['clouds'] = float(h['cloudCover'])
        # Wind speed
        h['wind_speed'] = float(h['windSpeed'])
        # Cardinal direction
        h['cardinal'] = self.cardinal(float(h['windDirection']))
        # Main weather
        code_day = str(h['weatherCode']) # int() to str() data
        code_day = self.fix_weather(daytime=h['daytime'], code=code_day) 
        w = tomorrow_codes["weatherCode"][code_day]
        h['main'] = self.fix_kindle_weather(w)
        # Add pop
        h['pop'] = round(float(h['precipitationProbability']) / 100,1)
        # Add 'in_clouds'
        if config['in_clouds'] == 'cloudCover':
            h['in_clouds'] = round(float(h['cloudCover']) / 100,1)
        elif config['in_clouds'] == 'probability':
            h['in_clouds'] = round(h['pop'],1) if 'pop' in h else 0
        else:
            h['in_clouds'] = 0
        return h

    def DailyForecast(self, day):
        config = self.config
        d = self.api_data['1d']['data']['timelines'][0]['intervals'][day]['values']
        s = self.api_data['1d']['data']['timelines'][0]['intervals'][day]['startTime']
        tomorrow_codes = self.tomorrow_codes
        # Time
        d['dt'] = self.conv_epoch(s)
        # Sunrise and Sunset
        d['sunrise'] = self.conv_epoch(d['sunriseTime']) if not d['sunriseTime'] == None else 0
        d['sunset'] = self.conv_epoch(d['sunsetTime']) if not d['sunsetTime'] == None else 0
        # daitime
        d['daytime'] = self.daytime(dt=d['dt'], sunrise=d['sunrise'], sunset=d['sunset'])
        # Moonrise and Moonset
        d['moonrise'] = self.conv_epoch(d['moonriseTime']) if not d['moonriseTime'] == None else 0
        d['moonset'] = self.conv_epoch(d['moonsetTime']) if not d['moonsetTime'] == None else 0
        # Temperature
        d['temp_day'] = float(d['temperature'])
        d['temp_min'] = float(d['temperatureMin'])
        d['temp_max'] = float(d['temperatureMax'])
        # Pressure
        d['pressure'] = float(d['pressureSeaLevel'])
        # Clouds
        d['clouds'] = float(d['cloudCover'])
        # Wind speed
        d['wind_speed'] = float(d['windSpeed'])
        # Cardinal direction
        d['cardinal'] = self.cardinal(float(d['windDirection']))
        # Add pop
        d['pop'] = round(float(d['precipitationProbability']) / 100,1)
        # Add 'in_clouds'
        if config['in_clouds'] == 'cloudCover':
            d['in_clouds'] = round(float(d['cloudCover']) / 100,1)
        elif config['in_clouds'] == 'probability':
            d['in_clouds'] = round(d['pop'],1) if 'pop' in d else 0
        else:
            d['in_clouds'] = 0
        # Main weather
        code_day = str(d['weatherCode']) # int() to str()
        code_day = self.fix_weather(daytime=d['daytime'], code=code_day) 
        w = tomorrow_codes["weatherCode"][code_day]    
        d['main'] = self.fix_kindle_weather(w)
        return d

    def fix_weather(self, daytime, code):
        db = ('1000', '1100', '1101', '10000')
        if code in db:
            if  daytime == True:
                # Daytime
                code = code + 'd'
            else:
                # Night time
                code = code + 'n'
            return code
        else:
            return code

    def daytime(self, dt, sunrise, sunset):
        config = self.config
        tz = config['tz']
        d = datetime.fromtimestamp(dt, tz)
        yr, mon, day, hr, mi, _, _, _, _ = d.timetuple()
        _dt = hr * 60 + mi
        d = datetime.fromtimestamp(sunrise, tz)
        yr, mon, day, hr, mi, _, _, _, _ = d.timetuple()
        _sunrise = hr * 60 + mi
        d = datetime.fromtimestamp(sunset, tz)
        yr, mon, day, hr, mi, _, _, _, _ = d.timetuple()
        _sunset = hr * 60 + mi
        if _dt > _sunrise and _dt < _sunset:
            return True
        else:
            return False
        
    def fix_kindle_weather(self, name):
        d = {
            'Sunny': 'ClearDay',
            'Clear Sky': 'ClearNight',
            'Mostly Clear Day': 'PartlyCloudyDay',
            'Mostly Clear Night': 'PartlyCloudyNight',
            'Partly Cloudy Day': 'PartlyCloudyDay',
            'Partly Cloudy Night': 'PartlyCloudyNight',
            'Mostly Cloudy': 'Cloudy',
            'Cloudy': 'Cloudy',
            'Fog': 'Fog',
            'Light Fog': 'Fog',
            'Drizzle': 'Drizzle',
            'Rain': 'Rain',
            'Light Rain': 'Rain',
            'Heavy Rain': 'Rain',
            'Snow': 'Snow',
            'Flurries': 'Wind',
            'Light Snow': 'Snow',
            'Heavy Snow': 'Snow',
            'Freezing Drizzle': 'Drizzle',
            'Freezing Rain': 'Rain',
            'Light Freezing Rain': 'Rain',
            'Heavy Freezing Rain': 'Rain',
            'Ice Pellets': 'Snow',
            'Heavy Ice Pellets': 'Snow',
            'Light Ice Pellets': 'Snow',
            'Thunderstorm': 'Thunderstorm'
        }
        return d[name]

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

    def conv_epoch(self, s):
        if not s == None:            
            a = datetime.fromisoformat(s)
            return int(a.timestamp())
        else:
            return s


## test API
#dumpAPI = 'output.json'
#with open(dumpAPI, 'r', encoding='utf-8') as f:
#    api_data = json.load(f)
#print('config',TomorrowIo(setting='setting.json', api_data=api_data).config, '\n')
#print('current',TomorrowIo(setting='setting.json', api_data=api_data).CurrentWeather(), '\n')
#print('hourly', TomorrowIo(setting='setting.json', api_data=api_data).HourlyForecast(0), '\n')
#print('daily', TomorrowIo(setting='setting.json', api_data=api_data).DailyForecast(1), '\n')
