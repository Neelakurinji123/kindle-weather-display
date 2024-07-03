#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Written by : krishna@hottunalabs.net
# Update     : 8 May 2024 


import time as t
import sys, re, json, io, os
from pathlib import Path
import zoneinfo
import locale
import shutil
from subprocess import Popen, PIPE
from wand.image import Image
from wand.display import display
from cairosvg import svg2png
from Modules import Maintenant, CurrentWeatherPane, HourlyWeatherPane, DailyWeatherPane, TwitterPane, GraphPane, GraphLabel, GraphLine
import SVGtools

# Working dir
this_file = os.path.realpath(__file__)
path = Path(this_file).parents[0]
os.chdir(str(path))

svgfile = "/tmp/KindleStation.svg"
pngfile = "/tmp/KindleStation.png"
pngtmpfile = "/tmp/.KindleStation.png"
flatten_pngfile = "/tmp/KindleStation_flatten.png"
error_image = "./img/error_service_unavailable.png"
i18nfile = "./config/i18n.json"
    
def svg_processing(p, text=str(), draw=str(), y=0):
    now = p.now
    tz = zoneinfo.ZoneInfo(p.config['timezone'])
    utc = zoneinfo.ZoneInfo('UTC')
    layout = p.config['layout']
    graph_objects = p.config['graph_objects']
    qr_png_val = None
    for s in layout:
        if s == 'maintenant':    
            a = Maintenant(p=p, y=y)
            text += a.text()
            draw += a.icon()
            y += 50
            #y += 40
        elif s == 'main':      
            if p.config['landscape'] == True:
                wordwrap = 18
                a = CurrentWeatherPane(p=p, y=y, wordwrap=wordwrap)
                text += a.text()
                draw += a.icon()
                start_hour, span, step, pitch = 3, 9, 3, 155
                a = HourlyWeatherPane(p=p, y=y, hour=start_hour, span=span, step=step, pitch=pitch)
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
            a = DailyWeatherPane(p=p, y=y, span=span, pitch=pitch)
            text += a.text()
            draw += a.icon()
            y += 280
        elif s == 'twitter':
            try:
                a = TwitterPane(p=p, y=y)
                _text, url, processing = a.text()
                if processing == True:
                    text += _text
                    qr_png_val = a.qrcode(url)
                else:
                    # Alternate layout
                    p.config['layout'] = p.config['twitter']['alternate']
                    p.config['graph_objects'] = graph_objects
                    text, draw, qr_png_val = svg_processing(p=p, text=text, draw=draw, y=y)
                    break
            except Exception as e:
                # Alternate layout
                print(e)
                p.config['layout'] = p.config['twitter']['alternate']
                p.config['graph_objects'] = graph_objects
                text, draw, qr_png_val = svg_processing(p=p, text=text, draw=draw, y=y)
                break
        elif s == 'graph':
            obj = graph_objects.pop()
            if p.config['landscape'] == True:
                # pane size(y=120)
                a = GraphPane(p=p, y=y+40, obj=obj)
                draw += a.draw()
                y += 120
            else:
                # pane size(y=120)
                a = GraphPane(p=p, y=y, obj=obj)
                draw += a.draw()
                y += 120 
        elif re.search('xlabel', s):
            if p.config['landscape'] == True:
                a = GraphLabel(p=p, y=y+25, s=s)
                text += a.text()
                y += 40
            else:
                a = GraphLabel(p=p, y=y, s=s)
                text += a.text()
                y += 20
        elif re.match(r'(padding[\+\-0-9]*)', s):
            y += int(re.sub('padding', '', s))
        elif re.search('h_line', s):
            a = GraphLine(p=p, y=y, obj=p.config['graph_lines'][s])
            draw += a.draw()
                       
    return text, draw, qr_png_val

def img_processing(p, svg, qr_png_val):
    now = p.now
    landscape = p.config['landscape']
    darkmode = p.config['darkmode']
    cloudconvert = p.config['cloudconvert']
    encoding = p.config['encoding']
    w = p.config['w']
    h = p.config['h'],
    state = CurrentWeatherPane(p=p).state
    try:
        b_png = io.BytesIO()
        #if cloudconvert == False and (encoding == 'iso-8859-1' or encoding == 'iso-8859-5'):
        if cloudconvert == False:
            svg2png(bytestring=svg, write_to=b_png, background_color="white", parent_width=w, parent_height=h)
            png_val = b_png.getvalue()
        elif cloudconvert == True:
            with open(svgfile, 'w') as f:
                f.write(svg)
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
            with open(pngfile, mode='rb') as f:
                png_val = f.read()
                with Image(width=800, height=600, background='white') as bg_img: 
                    with Image(blob=png_val) as fg_img:
                        bg_img.composite(fg_img, left=0, top=0)
                        bg_img.format = 'png'
                        img_blob = bg_img.make_blob('png')
                        fg_img.close()
                    bg_img.close()
                png_val = img_blob

    except Exception as e:
        print(e)

    # insert QR code
    if not qr_png_val == None:
        with Image(blob=png_val) as bg_img:
            with Image(blob=qr_png_val) as fg_img:
                fg_img.resize(150, 150)
                if landscape == True:
                    bg_img.composite(fg_img, left=15, top=430)
                else:
                    bg_img.composite(fg_img, left=15, top=600)
                bg_img.format = 'png'
            fg_img.close()
            img_blob = bg_img.make_blob('png')
        bg_img.close()
        png_val = img_blob

    if darkmode == 'True' or (darkmode == 'Auto' and (state == 'night' or state == 'polar_night')):
        with Image(blob=png_val) as img:
            img.negate(True,"all_channels")
            img.format = 'png'
            img_blob = img.make_blob('png')
        img.close()
        png_val = img_blob

    with Image(blob=png_val) as img:
        if landscape == True:
            img.rotate(90)
        img.alpha_channel_types = 'flatten'
        if darkmode == 'True' or (darkmode == 'Auto' and (state == 'night' or state == 'polar_night')):
            if p.config['system'] == 'openwrt':
                img.negate(True,"all_channels")
        img.save(filename=flatten_pngfile)
    img.close()

def main(setting, flag_dump, flag_config, flag_svg, flag_png):
    try:
        with open(setting, 'r') as f:
            a = json.load(f)['station']
            api = a['api']

        if api == 'OpenWeather':
            from OpenWeatherMapOnecallAPIv3 import OpenWeatherMap
            api_data = OpenWeatherMap(setting=setting).ApiCall()
            if not flag_dump == True:   
                p = OpenWeatherMap(setting=setting, api_data=api_data)
        elif api == 'Tomorrow.io':
            from TomorrowIoAPI import TomorrowIo
            #test
            #with open(setting_path + '/Tomorrow.ioAPI_output.json', 'r') as f:
            #    api_data = json.load(f)             
            api_data = TomorrowIo(setting=setting).ApiCall()
            if not flag_dump == True:
                p = TomorrowIo(setting=setting, api_data=api_data)    
        ## test: API data dump ##
        if flag_dump == True:
            output = path + '/' + api + '_API_output.json'
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(api_data, f, ensure_ascii=False, indent=4)
                exit(0)
        elif flag_config == True:
            output = path + '/' + api + '_config_output.json'
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(p.config, f, ensure_ascii=False, indent=4)
                exit(0)
        # Locale
        #locale.setlocale(locale.LC_TIME, p.config['locale'])
        text, draw, qr_png_val = svg_processing(p=p)
        # add footer
        s1 = p.config['city'] + ' - ' if p.config['sunrise_and_sunset'] == True else str()
        s2 = p.config['api']
        s = s1 + s2
        _s = SVGtools.text('end', '16', (p.config['w'] - 5), (p.config['h'] - 5), (s + ' API')).svg()
        text += SVGtools.fontfamily(font=p.config['font'], _svg=_s).svg()
        _svg = text + draw 
        svg =  SVGtools.format(encoding=p.config['encoding'], height=p.config['h'], width=p.config['w'], font=p.config['font'], _svg=_svg).svg()
        if flag_svg == True:
            output = svgfile
            with open(output, 'w', encoding='utf-8') as f:
                f.write(svg)
            f.close()    
            exit(0)
        else:
            img_processing(p=p, svg=svg, qr_png_val=qr_png_val)

    except Exception as e:
        print(e)
        shutil.copyfile(error_image, flatten_pngfile)
        exit(1)
    
    if flag_png == True:
        exit(0)
        
    # Display kindle
    kindleIP = '192.168.2.2'
    cmd = f'''`ssh root@{kindleIP} 'pidof powerd'` 
if [ "$p" != '' ]; then
    ssh root@{kindleIP} "/etc/init.d/powerd stop"
    ssh root@{kindleIP} "/etc/init.d/framework stop"
fi'''
    out = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).wait()
    cmd = f'scp {flatten_pngfile} root@{kindleIP}:/tmp'
    out = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).wait()
    cmd = f'ssh root@{kindleIP} \"cd /tmp; /usr/sbin/eips -c\"'
    out = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).wait()
    cmd = f'ssh root@{kindleIP} \"cd /tmp; /usr/sbin/eips -g {flatten_pngfile}\"'
    out = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).wait()

if __name__ == "__main__":
    flag_dump, flag_config, flag_svg, flag_png = False, False, False, False
    if 'dump' in sys.argv:
        flag_dump = True
        sys.argv.remove('dump')
    elif 'config' in sys.argv:
        flag_config = True
        sys.argv.remove('config')
    elif 'svg' in sys.argv:
        flag_svg = True
        sys.argv.remove('svg')
    elif 'png' in sys.argv:
        flag_png = True
        sys.argv.remove('png')

    # Use custom setting   
    if len(sys.argv) > 1:
        setting = sys.argv[1]
    else:
        setting = "setting.json" # Default setting
        
    main(setting, flag_dump, flag_config, flag_svg, flag_png)


