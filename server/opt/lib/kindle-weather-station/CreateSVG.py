#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Update     : 8 May 2024 


import time as t
import sys
import re
from pytz import timezone
import pytz
import locale
import shutil
from subprocess import Popen
from OpenWeatherMapOnecallAPIv3 import OpenWeatherMap
from Modules import Maintenant, CurrentWeatherPane, CurrentWeatherPane2, HourlyWeatherPane, DailyWeatherPane, TwitterPane, GraphPane, GraphLabel
import SVGtools

settings = "settings.json" # Default settings
svgfile = "/tmp/KindleStation.svg"
pngfile = "/tmp/KindleStation.png"
pngtmpfile = "/tmp/.KindleStation.png"
flatten_pngfile = "/tmp/KindleStation_flatten.png"
error_image = "./img/error_service_unavailable.png"
i18nfile = "./config/i18n.json"

    
def create_svg(p, svgfile):
    header, text, draw, footer = str(), str(), str(), str()
    layout = p.config['layout']

    # timezone setting
    now = p.now
    tz = timezone(p.config['timezone'])
    utc = pytz.utc
    f_svg = open(svgfile,"w", encoding=p.config['encoding'])
    layout = p.config['layout']
    graph_objects = p.config['graph_objects']
    x, y = 0, 0

    header += '''<?xml version="1.0" encoding="{}"?>
<svg xmlns="http://www.w3.org/2000/svg" height="800" width="600" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n'''.format(p.config['encoding'])
    header += '<g font-family="{}">\n'.format(p.config['font'])
    #svg_header += '<g font-family="{}">\n'.format("Chalkboard")
    #svg_header += '<g font-family="{}">\n'.format("Arial")

    def maintenant_pane(p, x, y, text, draw):
        # Maintenant: y=40        
        a = Maintenant(p=p, x=x, y=y)
        text += a.text()
        draw += a.icon()
        #y += 45
        y += 40
        return x, y, text, draw
        
    def main_pane(p, x, y, text, draw):
        # Current weather: size(x=365, y=480)
        offset, wordwrap = 35, 18
        a = CurrentWeatherPane(p=p, x=x+5, y=y, offset=offset, wordwrap=wordwrap)
        text += a.text()
        draw += a.icon()
        
        # Hourly weather: size(x=235, y=480)
        hour, span, step, pitch = 3, 12, 3, 155
        a = HourlyWeatherPane(p=p, x=x+370, y=y, hour=hour, span=span, step=step, pitch=pitch)
        text += a.text()
        draw += a.icon()
        y = y + 480
        return x, y, text, draw
        
    def main2_pane(p, x, y, text, draw):
        # Current weather: size(x=365, y=480)
        x, y, offset, wordwrap = x, y, 35, 100
        a = CurrentWeatherPane2(p=p, x=x+5, y=y, offset=offset, wordwrap=wordwrap)
        text += a.text()
        draw += a.icon()
        y += 340
        return x, y, text, draw
        
    def houly_pane(p, x, y, text, draw):
        # Hourly weather: size(x=235, y=480)
        hour, span, step, pitch = 3, 12, 3, 155
        a = HourlyWeatherPane(p=p, x=x+370, y=y, hour=hour, span=span, step=step, pitch=pitch)
        text += a.text()
        draw += a.icon()
        y += 480
        return x, y, text, draw
        
    def daily_pane(p, x, y, text, draw):
        # Daily weather: size(y=280)
        _x, y, span, pitch = 0, y, 4, 90
        a = DailyWeatherPane(p=p, x=_x, y=y-20, span=span, pitch=pitch)
        text += a.text()
        draw += a.icon()
        y += 280
        return x, y, text, draw

    def alternatePane(p, x, y, objects, text, draw):
        alternate = p.config['twitter']['alternate']

        for s in alternate:
            if s == 'daily':
                x, y, text, draw = daily_pane(p=p, x=x, y=y, text=text, draw=draw)
            elif s == 'graph':
                try:
                    obj = objects.pop()
                    x, y, text, draw = graph_pane(p=p, x=x, y=y, obj=obj, text=text, draw=draw)
                except Exception as e:
                    print(e)
            elif s == 'hourly_xlabel' or s == 'daily_xlabel':
                x, y, text, draw = label_pane(p=p, x=x, y=y, s=s, text=text, draw=draw)
            elif re.match(r'(padding[\+\-0-9]*)', s):
                y += int(re.sub('padding', '', s))
        return x, y, text, draw
        
    def twitter_pane(p, x, y, objects, text, draw):
        try:
            a = TwitterPane(p=p, x=x, y=y)
            _text, url, processing = a.text()
            if processing == True:
                text += _text
                draw += a.draw(url)
            else:
                # Alternate
                x, y, text, draw = alternatePane(p=p, x=x, y=y, objects=objects, text=text, draw=draw)
        except Exception as e:
            # Alternate
            print(e)
            x, y, text, draw = alternatePane(p=p, x=x, y=y, objects=objects, text=text, draw=draw)
            
        return x, y, text, draw
 
    def graph_pane(p, x, y, obj, text, draw):
        # pane size(y=120)
        #x, y = 40, 660
        a = GraphPane(p=p, x=x+40, y=y+60, obj=obj)
        draw += a.draw()
        y += 120
        return x, y, text, draw
        
    def label_pane(p, x, y, s, text, draw):
        #x, y = 40, 660?
        x, y = x, y
        a = GraphLabel(p=p, x=x+40, y=y-60, s=s)
        text += a.text()
        y += 20
        return x, y, text, draw
        
    objects = p.config['graph_objects']        
    for s in layout:
        if s == 'maintenant':
            x, y, text, draw = maintenant_pane(p=p, x=x, y=y, text=text, draw=draw)
        elif s == 'main':
            x, y, text, draw = main_pane(p=p, x=x, y=y, text=text, draw=draw)
        elif s == 'main2':
            x, y, text, draw = main2_pane(p=p, x=x, y=y, text=text, draw=draw)
        elif s == 'houly':
            x, y, text, draw = houly_pane(p=p, x=x, y=y, text=text, draw=draw)
        elif s == 'daily':
            x, y, text, draw = daily_pane(p=p, x=x, y=y, text=text, draw=draw)
        elif s == 'twitter':
            x, y, text, draw = twitter_pane(p=p, x=x, y=y, objects=objects, text=text, draw=draw)
        elif s == 'graph':
            obj = objects.pop()
            x, y, text, draw = graph_pane(p=p, x=x, y=y, obj=obj, text=text, draw=draw)
        elif s == 'hourly_xlabel' or s == 'daily_xlabel':
            x, y, text, draw = label_pane(p=p, x=x, y=y, s=s, text=text, draw=draw)
        elif re.match(r'(padding[\+\-0-9]*)', s):
            y += int(re.sub('padding', '', s))
            
    text += '</g>\n'
    footer += '</svg>' 
    f_svg.write(header + text + draw + footer)
    f_svg.close()


# image processing
def img_processing(p, svgfile, pngfile, pngtmpfile):
    now = p.now
    converter = p.config['converter']

    #if p.config['cloudconvert'] == False and (p.config['encoding'] == 'iso-8859-1' or p.config['encoding'] == 'iso-8859-5'):
    if p.config['cloudconvert'] == False:
        if converter == 'convert':
            a = ['convert', '-size', '600x800', '-background', 'white', '-depth', '8', svgfile, pngfile]
            out = Popen(a)
        elif converter == 'gm':
            a = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', \
                 '-resize', '600x800', '-colorspace', 'gray', '-type', 'palette', '-geometry', '600x800', svgfile, pngfile]
            out = Popen(a)
        else:
            print('Create a SVG file only.')

        
    elif p.config['cloudconvert'] == True:
        # Use cloudconvert API
        import cloudconvert
        import json

        with open('cloudconvert.json') as f:
            data = json.load(f)

        cloudconvert.configure(api_key=data['api_key'], sandbox=False)
        try:
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
            r = cloudconvert.Task.upload(file_name=svgfile, task=upload_task)
            r = cloudconvert.Task.find(id=upload_task_id)

            # convert
            job = cloudconvert.Job.create(payload={
                 "tasks": {
                     'convert-my-file': {
                         'operation': 'convert',
                         'input': r['id'],
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
            r = cloudconvert.Task.wait(id=exported_url_task_id) # Wait for job done
            file = r.get("result").get("files")[0]
            r = cloudconvert.download(filename=pngfile, url=file['url'])  # download and get filename

        except Exception as e:
            print(e)

    t.sleep(2)    
    if p.config['darkmode'] == 'True':
        out = Popen(['convert', '-flatten', pngfile, pngtmpfile])
        t.sleep(3)
        out = Popen(['convert', '-negate', pngtmpfile, flatten_pngfile])
    elif p.config['darkmode'] == 'Auto':
        if a['sunrise'] > now or a['sunset'] < now:
            out = Popen(['convert', '-flatten', pngfile, pngtmpfile])
            t.sleep(3)
            out = Popen(['convert', '-negate', pngtmpfile, flatten_pngfile])
        else:
            out = Popen(['convert', '-flatten', pngfile, flatten_pngfile])
    else:
        out = Popen(['convert', '-flatten', pngfile, flatten_pngfile])
        
    #t.sleep(3)

if __name__ == "__main__":
    # Use custom settings
    if len(sys.argv) > 1:
        settings = sys.argv[1]

    try:
        p = OpenWeatherMap(settings)
    except Exception as e:
        shutil.copyfile(error_image, flatten_pngfile)
        print(e)
        exit(1)
        
    # Hijri calendar
    if p.config['ramadhan'] == True:
        from hijri_converter import Hijri, Gregorian

    # Locale
    #locale.setlocale(locale.LC_TIME, p.config['locale'])
    create_svg(p=p, svgfile=svgfile)

    t.sleep(1)
    try:
        img_processing(p=p, svgfile=svgfile, pngfile=pngfile, pngtmpfile=pngtmpfile)
    except Exception as e:
        shutil.copyfile(error_image, flatten_pngfile)
        print(e)
        exit(1)