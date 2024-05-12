# Kindle Weather Display
This program is for a weather display on old Kindle 3 based on the original work by [Kindle-weather-station](https://gitlab.com/iero/Kindle-weather-station)

## Weather API
- Weather data from [OpenWeatherMap API](https://openweathermap.org/)

## Screenshots
<img src="sample_screenshots/kindle_weather-display.jpg" height="360" alt="Kindle 3 Screenshot" />&nbsp;


<kbd><img src="sample_screenshots/KindleStation_flatten_graph_1.png" height="360" alt="Kindle 3 Screenshot" /></kbd>&nbsp;
## Requirements
- Jailbroken Kindle 3: https://wiki.mobileread.com/wiki/Kindle_Hacks_Information
- server: Minimum 256M/100M OpenWrt router or SBC (e.g. OrangePi zero)
- server OS: Openwrt, Ubuntu and Debian, etc which work with Python3.
- USB port x1
- LAN port x1
- API key for OpenWeatherMap
- OpenWeatherMap One Call API subscription (v2.5)
- API key for CloudConvert for online image converter (optional)
- user account for X (twitter) (optional)


## Create API key for CloudConvert (optional)
Create API key with the following options:
- user.read: View your user data 
- user.write: Update your user data 
- task.read: View your task and job data 
- task.write: Update your task and job data


## Kindle PNG format
kindle requires special PNG format. Converting process is as follows:

```
 SVG image ------------> PNG image -------------> flattened PNG image
			converter:				converter:
			a)convert			 	a)convert	
			b)gm
			c)CloudConvert(online)
```
note:
`convert` is converter of ImageMagick.
`gm` is converter of graphicsMagick.
Both ImageMagick and graphicsMagick for Openwrt are lack of capabilities to manipulate SVG format.
Use CloudConvert.

## Set up server
### 1. Install the program
Copy `(github)/server/opt/lib/kindle-weather-station` to `(server)/opt/lib/kindle-weather-station`.

### 2.Install Graphics converters, Python3 and modules.
Grahpics: ImageMagick and graphicsMagick
Python3 (v3.11 or newer): 

### 3. Set up user account
In config directory, edit `OWM_config.json`, `cloudconvert.json`(optional) and `twitter_config.json`(optional)

### 4. Edit config files
Tempalate's names are settings_****.json.
Defailt config is settings.json


### 5. Install the program
#### Python3 module Requirements
- pytz
- requests
- setuptools
- pip
- twikit (optional)
- deep_translator (optional)
- qrcode (optional)
- cloudconvert (optional)
- hijri_converter (optional)

e.g.)
```
opkg update
opkg install python3 python3-pytz python3-requests python3-setuptools python3-pip
opkg install graphicsmagick
opkg install imagemagick
pip3 install twikit
pip3 install deep_translator
pip3 install qrcode
pip3 install cloudconvert
pip3 install hijri_converter
```

### 7. Network Time Synchronization
To retrieve data correctly, setup NTP server.

### 8. Test run
All set up finished, then try it.
```./CreateSVG.py```
or
```./CreateSVG.py settings_****.json```
Check `/etc/KindleStation_flatten.png`


### Install USB network
e.g.)
```
opkg install kmod-usb-net kmod-usb-net-rndis kmod-usb-net-cdc-ether usbutils
```

## Set up Kindle
Connect a USB cable to both the server and Kindle.
USB cable uses for network and power supply.

### 1. set up usbnet

```
 				LOCAL NETWORK				USB NETWORK			
  				e.g.(192.168.1.0/24)
 WAN <-> ROUTER <--------------> THE SERVER <------> KINDLE
								192.168.2.1/24		192.168.2.2/24
		
```
When usbnet setup is finished, then access to Kindle without password.
```
ssh root@192.168.2.2
```

### 2. setup dropbear Auth key
- Create the server's pub key.
- Set up the server's ssh environment.
- Copy the server's ssh pub key to Kindle.

e.g) 
```
cd /etc/dropbear
dropbearkey -y -f dropbear_rsa_host_key | grep "^ssh-rsa " > dropbear_rsa_host_key.pub
mkdir /root/.ssh
cd /root/.ssh
ln -s /etc/dropbear/dropbear_rsa_host_key id_dropbear
cd -
scp dropbear_rsa_host_key.pub root@192.168.2.2:/tmp
ssh root@192.168.2.2  # access to Kindle
cat /tmp/dropbear_rsa_host_key.pub >> /mnt/us/usbnet/etc/authorized_keys
exit
ssh root@192.168.2.2  # test passwordless login
```

### 3. Test run
```
cd /opt/lib/kindle-weather-station
./kindle-weather.sh [config.json]
```

## Layout
Kindle display size is 600 x 800.
Display layout is as follows:

| Module name      | Function                   | Size (Y-axis) |
|:-----------------|:---------------------------|--------------:|
| maintenant       | Time information           | 40            |
| main             | Current and hourly weather | 480           |
| main2            | Current weather            | 340           |
| hourly           | Hourly weather             | 480           |
| daily            | Daily weather              | 280           |
| graph            | Graph  or tile             | 120           |
| twitter          | Alert (Twitter)            | 280           |
| daily_xlabel     | Label for daily weather    | 20            |
| hourly_xlabel    | Label for hourly weather   | 20            |
| padding[-+0-9]*  | Insert spaces (Y axis only)|               |

Examples:
- maintenant + main + daily (40 + 480 + 280 = 800)
- maintenant + main2 + graph + \*\_xlabel + graph + \*\_xlabel + graph + padding20 (40 + 340 + 120 + 20 + 120 + 20 + 120 + 20 = 800)
- maintenant + main + graph + \*\_xlabel + graph + padding20 (40 + 480 + 120 + 20 + 120 + 20 = 800)
- maintenant + main + twitter (40 + 480 + 280 = 800)


## Modules

### maintenant

<kbd><img src="sample_screenshots/readme_imgs/maintenant_1.png" /></kbd>&nbsp;

- config
 - "city": "Granada"
 - "sunrise\_and\_sunset": "False"

<kbd><img src="sample_screenshots/readme_imgs/maintenant_2.png" /></kbd>&nbsp;

- config
 - "sunrise\_and\_sunset": "True"

### main

<kbd><img src="sample_screenshots/readme_imgs/main.png" /></kbd>&nbsp;

- config
 - "timezone": "Pacific/Auckland"
 - "encoding": "iso-8859-1"
 - "locale": "en_US.UTF-8"
 - "lat": "-77.8400829" 
 - "lon": "166.6445298"
 - "units": "metric"
 - "lang": "en"

### graph and tile

Available options are as follows:

- Daily Temperature
- Daily Precipitation
- Daily Weather
- Hourly Temperature
- Hourly Precipitation
- Moon Phase

#### graph 1: Daily Temperature and Moon Phase

<kbd><img src="sample_screenshots/readme_imgs/graph_1.png" /></kbd>&nbsp;

- config
 - graph\_objects": ["daily\_temperature", "moon\_phase"]
 - "ramadhan": "True"

#### graph 2: Daily Temperature and Daily Precipitation

<kbd><img src="sample_screenshots/readme_imgs/graph_2.png" /></kbd>&nbsp;

- config
 - "graph\_objects": ["daily\_temperature", "daily_precipitation"]

#### graph 3: Daily Weather and Moon Phase

<kbd><img src="sample_screenshots/readme_imgs/graph_3.png" /></kbd>&nbsp;

- config
 - "graph\_objects": ["daily\_weather", "moon\_phase"]
 - "ramadhan": "True"

#### graph 4: Hourly Temperature and Hourly Precipitation

<kbd><img src="sample_screenshots/readme_imgs/graph_4.png" /></kbd>&nbsp;

- config
 - "graph\_objects": ["hourly\_temperature", "hourly\_precipitation"]

### Twitter

<kbd><img src="sample_screenshots/readme_imgs/twitter.png" /></kbd>&nbsp;

- config
 - "twitter": {"caption": "ALERT", "screen\_name": "tenkijp", "translate": "True", "translate\_target": "en", "expiration": "3h", "alternate": ["graph", "daily\_xlabel", "graph"], "alternate_url": "https://tenki.jp/"}
  - screen_name: [@]Twitter Screen Name
  - translate: en(English), Other languages may work, but not sure.
  - expiration: Valid within Hours(h) or Minutes(m), otherwise use "alternate" layout.
  - alternate_url: If extract URL from Twitter is failed, use "alternate_url".
 - "twitter\_keywords": {"include": "heavy,thunder,disaster", "exclude": "sakura,zakura"}
  - include: If one of "include" keyword do match, display Twitter, otherwise  use "alternate" layout.
  - exclude: If one of "exclude" keyword do match, use "alternate" layout. 
 
 
# Set up time schedule

Edit crontab and restart cron

e.g.)

`crontab -e`

```
0 */2 * * * sh -c "/opt/lib/kindle-weather-station/kindle-weather.sh 2>>/tmp/kindle-weather-station.err"
0 1-23/2 * * * sh -c "/opt/lib/kindle-weather-station/kindle-weather.sh settings_twitter.json 2>>/tmp/kindle-weather-station.err"
```

```
# /etc/init.d/cron stop
# /etc/init.d/cron start
```

# Credits

- [OpenWeatherMap](https://openweathermap.org/) Weather data API
- [CloudConvert](https://cloudconvert.com/) An online file converter
- [X (Twitter)](https://twitter.com/home?lang=en) Twitter, Inc. is an American social media company.