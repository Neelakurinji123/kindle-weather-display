import time
import json
import requests
import xml.etree.ElementTree as ET
import geticon
import extras.getextraicon as extraicon

class OpenWeatherMap:
    icon = str()
    unit = dict()
    direction = str()

    def __init__(self, settings):

        self.t_now = time.time()

        d = dict()
        s = str()
        tree = ET.parse(settings)
        root = tree.getroot()

        # parse params file
        for service in root.findall('service'):
            if service.get('name') == 'station' :
                self.city = service.find('city').text
                self.t_timezone = service.find('timezone').text
                self.t_locale = service.find('locale').text
                self.encoding = service.find('encoding').text
                self.font = service.find('font').text
                self.sunrise_and_sunset = service.find('sunrise_and_sunset').text
                self.dark_mode = service.find('dark_mode').text
                self.api_key = service.find('api_key').text
                self.lat = service.find('lat').text
                self.lon = service.find('lon').text
                self.units = service.find('units').text
                self.lang = service.find('lang').text
                self.exclude = service.find('exclude').text

            s += '&units=' + self.units if self.units != '' else ''
            s += '&lang=' + self.lang if self.lang != '' else ''
            s += '&exclude=' + self.exclude if self.exclude != '' else ''

            url = 'https://api.openweathermap.org/data/2.5/onecall?' + 'lat=' + self.lat + '&lon=' + self.lon + s + '&appid=' + self.api_key

        self.onecall = requests.get(url).json()
        OpenWeatherMap.unit = self.set_unit(self.units)


    def current_weather(self):

        # current data
        # list - 0:time  1:id  2:weather  3:description  4:icon  5:temp  6:pressure  7:humidity  8:wind_speed  9:wind_direction  10:clouds
        #        11:sunrise  12:sunset  13:precipitation  14:probability of precipitation  15:gust  16:rain or snow
        #
        d = self.onecall

        dat = [d['current']['dt'],
               d['current']['weather'][0]['id'],
               d['current']['weather'][0]['main'],
               d['current']['weather'][0]['description'],
               d['current']['weather'][0]['icon'],
               d['current']['temp'],
               d['current']['pressure'],
               d['current']['humidity'],
               d['current']['wind_speed'],
               self.wind_direction(d['current']['wind_deg']),
               d['current']['clouds'],
               d['current']['sunrise'],
               d['current']['sunset']]

        # hourly precipitation
        #a = [(i, float(x['precipitation'])) for i, x in enumerate(d['minutely']) if i < 60]
        #dat += [sum([y for x, y in a])]
        dat += [None]

        # hourly probability of precipitation
        dat += [float(d['hourly'][1]['pop'])]

       # gust
        if 'wind_gust' in d['current']['weather'][0]:
            dat += [float(d['current']['wind_gust'])]
        else:
            dat += [None]

        # rain or snow past a hour
        if 'rain' in d['current']['weather'][0]:
            dat += [float(['current']['rain'])]
        elif 'snow' in d['current']['weather'][0]:
            dat += [float(d['current']['snow'])]
        else:
            dat += [None]

        # fix icon
        p = {'id': dat[1], 'weather': dat[2], 'description': dat[3], 'icon': dat[4]}
        dat[2] = self.fix_icon(**p)

        OpenWeatherMap.icon = self.add_icon(dat[2])

        return dat


    def forecast_hourly(self, hour):

        # forecast data
        # list - 0:time  1:id  2:weather  3:description  4:icon  5:temp  6:clouds  7:pop  8:wind gust  9:rain or snow
        d = self.onecall
        d_hourly = d['hourly'][hour]
        dat = [int(d_hourly['dt']), int(d_hourly['weather'][0]['id']), str(d_hourly['weather'][0]['main']),
               str(d_hourly['weather'][0]['description']), str(d_hourly['weather'][0]['icon']),
               float(d_hourly['temp']), float(d_hourly['clouds']), float(d_hourly['pop'])]

       # gust
        if 'wind_gust' in d_hourly:
            dat += [float(d_hourly['wind_gust'])]
        else:
            dat += [None]

        # rain or snow past a hour
        if 'rain' in d_hourly:
            dat += [float(d_hourly['rain']['1h'])]
        elif 'snow' in d_hourly:
            dat += [float(d_hourly['snow']['1h'])]
        else:
            dat += [None]

        # fix icon
        p = {'id': dat[1], 'weather': dat[2], 'description': dat[3], 'icon': dat[4]}
        dat[2] = self.fix_icon(**p)

        OpenWeatherMap.icon = self.add_icon(dat[2])

        return dat

    def forecast_daily(self, day):

        # forecast data
        # list - 0:time  1:id  2:weather  3:description  4:icon  5:temp day 6:temp min  7:temp max  8:clouds  9: probability of precipitation
        #        10:precipitation  11:wind gust  12:rain or snow
        d = self.onecall
        d_daily = d['daily'][day]
        dat = [int(d_daily['dt']), int(d_daily['weather'][0]['id']), str(d_daily['weather'][0]['main']),
               str(d_daily['weather'][0]['description']), str(d_daily['weather'][0]['icon']),
               float(d_daily['temp']['day']), float(d_daily['temp']['min']), float(d_daily['temp']['max']),
               float(d_daily['clouds']), float(d_daily['pop'])]

       # gust
        if 'wind_gust' in d_daily:
            dat += [float(d_daily['wind_gust'])]
        else:
            dat += [None]

        # rain or snow past a hour
        if 'rain' in d_daily:
            dat += [float(d_daily['rain'])]
        elif 'snow' in d_daily:
            dat += [float(d_daily['snow'])]
        else:
            dat += [None]

        # fix icon
        p = {'id': dat[1], 'weather': dat[2], 'description': dat[3], 'icon': dat[4]}
        dat[2] = self.fix_icon(**p)

        OpenWeatherMap.icon = self.add_icon(dat[2])

        return dat


    def fix_icon(self, id, weather, description, icon):

        day_or_night = 'day' if icon[-1] == 'd' else 'night'

        if weather == 'Clear':
            dat = weather + '-' + day_or_night
        elif weather == 'Clouds' and description == 'few clouds':
            dat = 'Few-clouds' + '-' + day_or_night
        else:
            dat = weather

        if weather == 'Snow' and (int(id) == 611 or int(id) == 612 or int(id) == 613):
            dat = 'Sleet'
        elif weather == 'Snow' and (int(id) == 602 or int(id) == 622):
            dat = 'Snow2'

        return dat


    def wind_direction(self, degree):
        if degree >= 348.75 or degree <= 11.25:
            s = 'N'
        elif 11.25 < degree < 33.75:
            s = 'NNE'
        elif 33.75 <= degree <= 56.25:
            s = 'NE'
        elif 56.25 < degree < 78.75:
            s = 'ENE'
        elif 78.75 <= degree <= 101.25:
            s = 'E'
        elif 101.25 < degree < 123.75:
            s = 'ESE'
        elif 123.75 <= degree <= 146.25:
            s = 'SE'
        elif 146.25 < degree < 168.75:
            s = 'SSE'
        elif 168.75 <= degree <= 191.25:
            s = 'S'
        elif 191.25 < degree < 213.75:
            s = 'SSW'
        elif 213.75 <= degree <= 236.25:
            s = 'SW'
        elif 236.25 < degree < 258.75:
            s = 'WSW'
        elif 258.75 <= degree <= 281.25:
            s = 'W'
        elif 281.25 < degree < 303.75:
            s = 'WNW'
        elif 303.75 <= degree <= 326.25:
            s = 'NW'
        elif 326.25 < degree < 348.75:
            s = 'NNW'

        return s


    def add_icon(self, s):
        if s == 'Clear-day':
            if ("getClearDay" in dir(extraicon)) == True: return extraicon.getClearDay()
            else: return geticon.getClearDay()
        elif s == 'Clear-night':
            if ("getClearNight" in dir(extraicon)) == True: return extraicon.getClearNight()
            else: return geticon.getClearNight()
        elif s == 'Rain':
            if ("getRain" in dir(extraicon)) == True: return extraicon.getRain()
            else: return geticon.getRain()
        elif s == 'Drizzle':
            if ("getDrizzle" in dir(extraicon)) == True: return extraicon.getDrizzle()
            else: return geticon.getRain()
        elif s == 'Thunderstorm':
            if ("getThunderstorm" in dir(extraicon)) == True: return extraicon.getThunderstorm()
            else: return geticon.getRain()
        elif s == 'Snow':
            if ("getSnow" in dir(extraicon)) == True: return extraicon.getSnow()
            else: return geticon.getSnow()
        elif s == 'Sleet':
            if ("getSleet" in dir(extraicon)) == True: return extraicon.getSleet()
            else: return geticon.getRain()
        elif s == 'Wind':
            if ("getWind" in dir(extraicon)) == True: return extraicon.getWind()
            else: return geticon.getWind()
        elif s == 'Clouds':
            if ("getCloudy" in dir(extraicon)) == True: return extraicon.getCloudy()
            else: return geticon.getCloudy()
        elif s == 'Few-clouds-day':
            if ("getPartlyCloudyDay" in dir(extraicon)) == True: return extraicon.getPartlyCloudyDay()
            else: return geticon.getPartlyCloudyDay()
        elif s == 'Few-clouds-night':
            if ("getPartlyCloudyNight" in dir(extraicon)) == True: return extraicon.getPartlyCloudyNight()
            else: return geticon.getPartlyCloudyNight()
        elif s == 'Mist':
            if ("getMist" in dir(extraicon)) == True: return extraicon.getMist()
            else: return geticon.getFog()
        elif s == 'Smoke':
            if ("getSmoke" in dir(extraicon)) == True: return extraicon.getSmoke()
            else: return geticon.getFog()
        elif s == 'Haze':
            if ("getHaze" in dir(extraicon)) == True: return extraicon.getHaze()
            else: return geticon.getFog()
        elif s == 'Dust':
            if ("getDust" in dir(extraicon)) == True: return extraicon.getDust()
            else: return geticon.getFog()
        elif s == 'Fog':
            if ("getFog" in dir(extraicon)) == True: return extraicon.getFog()
            else: return geticon.getFog()
        elif s == 'Sand':
            if ("getSand" in dir(extraicon)) == True: return extraicon.getSand()
            else: return geticon.getFog()
        elif s == 'Dust':
            if ("getDust" in dir(extraicon)) == True: return extraicon.getDust()
            else: return geticon.getFog()
        elif s == 'Ash':
            if ("getAsh" in dir(extraicon)) == True: return extraicon.getAsh()
            else: return geticon.getFog()
        elif s == 'Squall':
            if ("getSquall" in dir(extraicon)) == True: return extraicon.getSquall()
            else: return geticon.getRain()
        elif s == 'Tornado':
            if ("getTornado" in dir(extraicon)) == True: return extraicon.getTornado()
            else: return geticon.getWind()
        elif s == 'Cyclone':
            if ("getCyclone" in dir(extraicon)) == True: return extraicon.getCyclone()
            else: return geticon.getWind()
        elif s == 'Snow2':
            if ("getSnow2" in dir(extraicon)) == True: return extraicon.getSnow2()
            else: return geticon.getSnow()
        elif s == 'Sunrise':
            if ("getSunrise" in dir(extraicon)) == True: return extraicon.getSunrise()
            else: return None
        elif s == 'Sunset':
            if ("getSunset" in dir(extraicon)) == True: return extraicon.getSunset()
            else: return None


    def set_unit(self, s):
        if self.units == 'metric':
            dat = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'C'}
        elif self.units == 'imperial':
            dat = {'pressure': 'hPa', 'wind_speed': 'mph', 'temp': 'F'}
        else:
            dat = {'pressure': 'hPa', 'wind_speed': 'm/s', 'temp': 'K'}

        return dat

# test
#a = OpenWeatherMap('settings-San-Francisco.xml')
#print(a.current_weather(), '\n')
#print(a.forecast_hourly(1), '\n')
#print(a.forecast_daily(1), '\n')

#print(type(a.forecast_daily(1)),'\n')
#print(a.icon, '\n')
#print(type(a.forecast_daily(3)),'\n')
#print(a.icon, '\n')
#print(type(a.forecast_daily(5)),'\n')
#print(a.lang, '\n')
#print(a.unit, '\n')
