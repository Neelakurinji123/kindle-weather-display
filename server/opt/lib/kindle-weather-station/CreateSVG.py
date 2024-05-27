#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Update     : 8 May 2024 


import time as t
import sys, re, json, io
from pytz import timezone
import locale
import shutil
from subprocess import Popen
from wand.image import Image
from wand.display import display
from Modules import Maintenant, CurrentWeatherPane, HourlyWeatherPane, DailyWeatherPane, TwitterPane, GraphPane, GraphLabel, GraphLine
import SVGtools

settings = "settings.json" # Default settings
svgfile = "/tmp/KindleStation.svg"
pngfile = "/tmp/KindleStation.png"
pngtmpfile = "/tmp/.KindleStation.png"
flatten_pngfile = "/tmp/KindleStation_flatten.png"
error_image = "./img/error_service_unavailable.png"
i18nfile = "./config/i18n.json"
    
def svg_processing(p, text=str(), draw=str(), y=0):
    now = p.now
    tz = timezone(p.config['timezone'])
    utc = timezone('utc')
    #f_svg = open(svgfile,"w", encoding=p.config['encoding'])
    layout = p.config['layout']
    graph_objects = p.config['graph_objects']
    # Landscape's paper layout
    variant = 1 if p.config['landscape'] == True else None
    for s in layout:
        if s == 'maintenant':    
            a = Maintenant(p=p, y=y, variant=None)
            text += a.text()
            draw += a.icon()
            y += 50
            #y += 40
        elif s == 'main':      
            if p.config['landscape'] == True:
                wordwrap = 18
                a = CurrentWeatherPane(p=p, y=y, wordwrap=wordwrap, variant=None)
                text += a.text()
                draw += a.icon()
                start_hour, span, step, pitch = 3, 9, 3, 155
                a = HourlyWeatherPane(p=p, y=y, hour=start_hour, span=span, step=step, pitch=pitch, variant=None)
                text += a.text()
                draw += a.icon()
                y += 340
            else:
                # Current weather: size(x=365, y=480)
                wordwrap = 18
                a = CurrentWeatherPane(p=p, y=y, wordwrap=wordwrap)
                text += a.text()
                draw += a.icon()
                # Hourly weather: size(x=235, y=480)
                start_hour, span, step, pitch = 3, 12, 3, 155   
                a = HourlyWeatherPane(p=p, y=y, hour=start_hour, span=span, step=step, pitch=pitch)        
                text += a.text()
                draw += a.icon()
                y += 490
        elif s == 'daily':
            # Daily weather: size(y=280)
            span, pitch = 4, 90
            a = DailyWeatherPane(p=p, y=y, span=span, pitch=pitch, variant=variant)
            text += a.text()
            draw += a.icon()
            y += 280
        elif s == 'twitter':
            try:
                a = TwitterPane(p=p, y=y, variant=None)
                _text, url, processing = a.text()
                if processing == True:
                    text += _text
                    draw += a.draw(url)
                else:
                    #layout = p.config['layout']
                    p.config['layout'] = p.config['twitter']['alternate']
                    text, draw = svg_processing(p=p, text=text, draw=draw, y=y)
                    # Alternate layout
                    #y, text, draw = alternatePane(p=p, y=y, objects=graph_objects, text=text, draw=draw)
            except Exception as e:
                # Alternate layout
                print(e)
                #p.config['layout'] = p.config['twitter']['alternate']
               # text, draw = svg_processing(p=p, text=text, draw=draw, y=y)
                ##y, text, draw = alternatePane(p=p, y=y, objects=graph_objects, text=text, draw=draw)
        elif s == 'graph':
            obj = graph_objects.pop()
            if p.config['landscape'] == True:
                # pane size(y=120)
                a = GraphPane(p=p, y=y+40, obj=obj, variant=None)
                draw += a.draw()
                y += 120
            else:
                # pane size(y=120)
                a = GraphPane(p=p, y=y, obj=obj, variant=None)
                draw += a.draw()
                y += 120 
        #elif s == 'hourly_xlabel' or s == 'daily_xlabel':
        elif re.search('xlabel', s):
            if p.config['landscape'] == True:
                a = GraphLabel(p=p, y=y+25, s=s, variant=None)
                text += a.text()
                y += 40
            else:
                a = GraphLabel(p=p, y=y, s=s, variant=None)
                text += a.text()
                y += 20
        elif re.match(r'(padding[\+\-0-9]*)', s):
            y += int(re.sub('padding', '', s))
        elif re.search('h_line', s):
            a = GraphLine(p=p, y=y, obj=p.config['graph_lines'][s], variant=None)
            draw += a.draw()
                       
    #text += '</g>\n'
    
   
    #f_svg.write(header + text + draw + footer)
    #f_svg.close()
    return text, draw

def create_svg(p, text, draw, svgfile=None):
    width, height = (800, 600) if p.config['landscape'] == True else (600, 800)
    header = '''<?xml version="1.0" encoding="{}"?>
<svg xmlns="http://www.w3.org/2000/svg" height="{}" width="{}" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n'''.format(p.config['encoding'], height, width)
    header += '<g font-family="{}">\n'.format(p.config['font'])
    #svg_header += '<g font-family="{}">\n'.format("Chalkboard")
    #svg_header += '<g font-family="{}">\n'.format("Arial")
    
    s1 = p.config['city'] + ' - ' if p.config['sunrise_and_sunset'] == True else str()
    s2 = p.config['api']
    s = s1 + s2
    a = '<g font-family="{}">\n'.format(p.config['font'])
    a += SVGtools.text('end', '16px', (width - 5), (height - 5), (s + ' API')).svg()
    #a += SVGtools.text2('end',  'bold', '16px', (800 - 5), (600 - 5), s).svg()
    text +=  a  + '</g>\n'
    footer = '</svg>'
    converter = p.config['converter']
    if converter == 'cairosvg':
        return header + text + draw + footer
    else:
        f_svg = open(svgfile,"w", encoding=p.config['encoding'])
        f_svg.write(header + text + draw + footer)
        f_svg.close()

# image processing
def img_processing(p, pngfile, svgfile=None, pngtmpfile=None, svg=None):
    now = p.now
    converter = p.config['converter']
    landscape = p.config['landscape']
    darkmode = p.config['darkmode']
    cloudconvert = p.config['cloudconvert']
    encoding = p.config['encoding']
    state = CurrentWeatherPane(p=p).state
    try:
        #if cloudconvert == False and (encoding == 'iso-8859-1' or encoding == 'iso-8859-5'):
        if cloudconvert == False:
            if converter == 'convert' and landscape == True:
                with Image(filename=svgfile) as img:
                    img.background_color = 'white'
                    img.depth = 8
                    img.width = 800
                    img.height = 600
                    img.save(filename=pngfile)
            elif converter == 'convert':
                with Image(filename=svgfile) as img:
                    img.background_color = 'white'
                    img.depth = 8
                    img.width = 600
                    img.height = 800
                    img.save(filename=pngfile)
            elif converter == 'gm' and landscape == True:
                #a = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', '-font', 'Droid Sans', \
                a = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', \
                     '-resize', '800x600', '-colorspace', 'gray', '-type', 'palette', '-geometry', '600x800', svgfile, pngfile]
                out = Popen(a)
            elif converter == 'gm':
                a = ['gm', 'convert', '-size', '600x800', '-background', 'white', '-depth', '8', \
                     '-resize', '600x800', '-colorspace', 'gray', '-type', 'palette', '-geometry', '600x800', svgfile, pngfile]
                out = Popen(a)
            elif converter == 'rsvg-convert' and landscape == True:
                a = ['rsvg-convert', '-w', '800', '-h', '600', '-b', 'white', '-f', 'png', svgfile, '-o', pngfile]
                out = Popen(a)
            elif converter == 'rsvg-convert':
                a = ['rsvg-convert', '-w', '600', '-h', '800', '-b', 'white', '-f', 'png', svgfile, '-o', pngfile]
                out = Popen(a)
            elif converter == 'cairosvg' and landscape == True:
                from cairosvg import svg2png
                svg2png(bytestring=svg, write_to=pngfile, background_color="white", parent_width=800, parent_height=600)
            elif converter == 'cairosvg':
                from cairosvg import svg2png
                #png = io.BytesIO()
                svg2png(bytestring=svg, write_to=pngfile, background_color="white", parent_width=600, parent_height=800)
                # test
                #with open(pngfile, 'wb', buffering=0) as f:
                #    f.write(png.getbuffer())
            else:
                print('Create a SVG file only.')
                exit(0)
        elif cloudconvert == True:
            # Use cloudconvert API
            import cloudconvert
            with open('./config/cloudconvert.json') as f:
                data = json.load(f)

            cloudconvert.configure(api_key=data['api_key'], sandbox=False)
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
    if darkmode == 'True':
        if landscape == True:
            with Image(filename=pngfile) as img:
                with img.clone() as i:
                    i.rotate(90)
                    i.alpha_channel_types = 'flatten'
                    i.negate(True,"all_channels")
                    i.save(filename=flatten_pngfile)
            #out = Popen(['convert', '-rotate', '+90', '-flatten', pngfile, flatten_pngfile])
        else:
            with Image(filename=pngfile) as img:
                with img.clone() as i:
                    i.alpha_channel_types = 'flatten'
                    i.negate(True,"all_channels")
                    i.save(filename=flatten_pngfile)
            #out = Popen(['convert', '-flatten', pngfile, pngtmpfile])
        #t.sleep(3)
        #out = Popen(['convert', '-negate', pngtmpfile, flatten_pngfile])
    elif darkmode == 'Auto':
        if state == 'day' or  state == 'midnight_sun':
            if landscape == True:
                with Image(filename=pngfile) as img:
                    with img.clone() as i:
                        i.rotate(90)
                        i.alpha_channel_types = 'flatten'
                        i.save(filename=flatten_pngfile)
                #out = Popen(['convert', '-rotate', '+90', '-flatten', pngfile, flatten_pngfile])
            else:
                with Image(filename=pngfile) as img:
                    with img.clone() as i:
                        i.alpha_channel_types = 'flatten'
                        i.save(filename=flatten_pngfile)
                #out = Popen(['convert', '-flatten', pngfile, pngtmpfile])
        else:
            if landscape == True:
                with Image(filename=pngfile) as img:
                    with img.clone() as i:
                        i.rotate(90)
                        i.alpha_channel_types = 'flatten'
                        i.negate(True,"all_channels")
                        i.save(filename=flatten_pngfile)
                #out = Popen(['convert', '-rotate', '+90', '-flatten', pngfile, flatten_pngfile])
            else:
                with Image(filename=pngfile) as img:
                    with img.clone() as i:
                        i.alpha_channel_types = 'flatten'
                        i.negate(True,"all_channels")
                        i.save(filename=flatten_pngfile)
                #out = Popen(['convert', '-flatten', pngfile, pngtmpfile])
            #t.sleep(3)
            #out = Popen(['convert', '-negate', pngtmpfile, flatten_pngfile])
    else:
        if landscape == True:
            #with Image(filename=pngfile) as img:
            #    with img.clone() as i:
            #        i.rotate(90)
            #        i.alpha_channel_types = 'flatten'
            #        i.save(filename=flatten_pngfile)
            out = Popen(['convert', '-rotate', '+90', '-flatten', pngfile, flatten_pngfile])
        else:
            #with Image(filename=pngfile) as img:
            #    with img.clone() as i:
            #        i.alpha_channel_types = 'flatten'
            #        i.save(filename=flatten_pngfile)
            out = Popen(['convert', '-flatten', pngfile, pngtmpfile])

if __name__ == "__main__":
    flag_dump, flag_config = False, False
    if 'dump' in sys.argv:
        flag_dump = True
        sys.argv.remove('dump')
    elif 'config' in sys.argv:
        flag_config = True
        sys.argv.remove('config')

    # Use custom settings    
    if len(sys.argv) > 1:
        settings = sys.argv[1]

    try:
        with open(settings, 'r') as f:
            a = json.load(f)['station']
            api = a['api']   
        if api == 'OpenWeather':
            from OpenWeatherMapOnecallAPIv3 import OpenWeatherMap
            api_data = OpenWeatherMap(settings).ApiCall()
            if not flag_dump == True:   
                p = OpenWeatherMap(settings=settings, api_data=api_data)
        elif api == 'Tomorrow.io':
            from TomorrowIoAPI import TomorrowIo
            #test
            #with open('Tomorrow.ioAPI_output.json', 'r') as f:
            #    api_data = json.load(f)             
            api_data = TomorrowIo(settings).ApiCall()
            if not flag_dump == True:
                p = TomorrowIo(settings=settings, api_data=api_data)     
        ## test: API data dump ##
        if flag_dump == True:
            output = api + 'API' + '_output.json'
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(api_data, f, ensure_ascii=False, indent=4)
                exit(0)
        elif flag_config == True:
            output = settings + '_' + api + '_output.json'
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(p.config, f, ensure_ascii=False, indent=4)
                exit(0)
        
        # Locale
        #locale.setlocale(locale.LC_TIME, p.config['locale'])
        text, draw = svg_processing(p=p)
        converter = p.config['converter']
        if converter == 'cairosvg':
            svg = create_svg(p=p, text=text, draw=draw)
            img_processing(p=p, pngfile=pngfile, svg=svg)
        else:
            create_svg(p=p, svgfile=svgfile, text=text, draw=draw)
            #create_svg(p, svgfile, svg)
            t.sleep(1)
            img_processing(p=p, svgfile=svgfile, pngfile=pngfile, pngtmpfile=pngtmpfile)

    except Exception as e:
        print(e)
        shutil.copyfile(error_image, flatten_pngfile)
        exit(1)
