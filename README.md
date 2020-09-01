# kindle-weather-display

This repo is display weather information on old kindle 3, based on the original work by [Kindle-weather-station](https://gitlab.com/iero/Kindle-weather-station).

## Features
* weather information is based on [OpenWeatherMap API](https://openweathermap.org/)
* current weather, 3 hour forecast and 3 day forecast
* any locales, languages and units

### Kindle 3 and TV-box (Armbian)
<img src="screenshot-kindle-weather.jpg" width="300" alt="Kindle 3 screenshot" />

## Setup
### kindle
1. jailbreak your Kindle
2. copy kindle/kindle-weather to /mnt/us folder
3. setup cron
5. setup usbnet: rename to /mnt/us/usbnet/auto
4. optionally install kindle-debian, system can improve

### server
1. get free subscription plan from openweathermap.org
2. copy host-server/var/lib/kindle-weather-host to /var/lib folder
3. install packages and setup (eg. debian buster)
4. install python3 modules: pytz, requests
5. setup font
6. setup cron

```
    image processors:
    apt install imagemagick imagemagick-6-common imagemagick-6.q16 \
      imagemagick-common libgraphicsmagick-q16-3 libmagickcore-6.q16-6 \
      libmagickcore-6.q16-6-extra libmagickwand-6.q16-6 pngcrush

    web server:
    apt install nginx-light

    firewall:
    apt install shorewall

    font:
    apt install fontconfig

    copy ttf font to /root/.fonts folder
    fc-cache -v -f
```

## setting
Edit settings.xml

## internet access
Old system is potential security risk in generally. But in the case of internet access is as folloings:

### server
Enable masquerade or snat:
```
/etc/shorewall/snat

MASQUERADE		192.168.2.0/24		<interface>
```
systemctl reload shorewall

### kindle
```
ip route add default via 192.168.2.1
echo 'nameserver 8.8.8.8' >> /etc/resolv.conf

#test
ping google.com
```

## Option
* [kindle-debian](https://mega.nz/folder/4XAlBK7Y#cSr2Gq8KxL6LkRe4SB0hqQ)
