#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import SVGtools

def test(data, _x, _y):
    encode = 'iso-8859-1'
    height = 450
    width = 450
    header = f'''<?xml version="1.0" encoding="{encode}"?>
<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n'''
    x = [s[0] for s in data]
    y = [s[1] for s in data]
    c = str()
    _svg = SVGtools.spline(data).svg()
    for i in range(len(data)):
        c += SVGtools.circle(x[i], y[i], 10, 'blue', 3, 'none').svg()
    svg = header + _svg + c + '</svg>\n'
    with open('test_spline.svg', 'w') as f:
        f.write(svg)
    f.close()
    _svg = SVGtools.spline(lst=data, _x=_x, _y=_y, stroke='rgb(105,105,105)', stroke_width=5, fill='rgb(211,211,211)').svg()
    svg = header + _svg + '</svg>\n'
    with open('test_spline_fill.svg', 'w') as f:
        f.write(svg)
    f.close()
    
if __name__ == "__main__":
    data = [(100, 200), (150, 120), (240, 150), (275, 100), (350, 175)]
    _x, _y = 100, 250
    test(data, _x, _y)  
