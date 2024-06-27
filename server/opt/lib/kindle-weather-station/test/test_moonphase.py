from math import pi, sin, cos
from cairosvg import svg2png

class Phase:
    def __init__(self, r, rx, ry, lat):
        self.r = r
        self.rx = rx
        self.ry = ry
        self.lat = lat
    
    def moon(self, ra1, ra2, ra3, rad, darkmode, cairo_fix):
        if self.lat > 0:
            if pi * 0.5 > rad >= 0:  # new moon to first quarter
                m = (pi * 0.5 - rad) / (pi * 0.5)
                px1 = cos(pi * 0.5 + m) * self.r + self.rx
                py1 = sin(pi * 0.5 + m) * self.r + self.ry
                px2 = cos(pi * 0.5 + m) * self.r + self.rx
                py2 = -sin(pi * 0.5 + m) * self.r + self.ry
                flag1, flag2 = (1, 0) if darkmode == True else (0, 1)
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 1 {px1} {py1}z'
                p = 'ps1'
            elif pi > rad >= pi * 0.5:  # first quarter to full moon
                if cairo_fix == True:
                    m = 0
                    flag1, flag2 = (1, 1) if darkmode == True else (0, 0)
                else:
                    m = (rad - pi * 0.5) / (pi * 0.5)
                    flag1, flag2 = (0, 0) if darkmode == True else (1, 1)
                px1 = cos(pi * 0.5 - m) * self.r + self.rx
                py1 = sin(pi * 0.5 - m) * self.r + self.ry
                px2 = cos(pi * 0.5 - m) * self.r + self.rx
                py2 = -sin(pi * 0.5 - m) * self.r + self.ry
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 0 {px1} {py1}z'
                p = 'ps2'
            elif pi * 1.5 > rad >= pi:  # full moon to third quarter
                if cairo_fix == True:
                    m = 0
                    flag1, flag2 = (1, 1) if darkmode == True else (0, 0)
                else:
                    m = (pi * 1.5 - rad) / (pi * 0.5)
                    flag1, flag2 = (0, 0) if darkmode == True else (1, 1)
                px1 = cos(pi * 1.5 - m) * self.r + self.rx
                py1 = sin(pi * 1.5 - m) * self.r + self.ry
                px2 = cos(pi * 1.5 - m) * self.r + self.rx
                py2 = -sin(pi * 1.5 - m) * self.r + self.ry
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 0 {px1} {py1}z'
                p = 'ps3'
            else:  # third quarter to new moon
                m = (rad - pi * 1.5) / (pi * 0.5)
                px1 = cos(pi * 1.5 + m) * self.r + self.rx
                py1 = sin(pi * 1.5 + m) * self.r + self.ry
                px2 = cos(pi * 1.5 + m) * self.r + self.rx
                py2 = -sin(pi * 1.5 + m) * self.r + self.ry
                flag1, flag2 = (1, 0) if darkmode == True else (0, 1)
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 1 {px1} {py1}z'
                p = 'ps4'
        else:
            if pi * 0.5 > rad >= 0:  # new moon to first quarter
                m = (pi * 0.5 - rad) / (pi * 0.5)
                px1 = cos(pi * 1.5 + m) * self.r + self.rx
                py1 = sin(pi * 1.5 + m) * self.r + self.ry
                px2 = cos(pi * 1.5 + m) * self.r + self.rx
                py2 = -sin(pi * 1.5 + m) * self.r + self.ry
                flag1, flag2 = (1, 0) if darkmode == True else (0, 1)
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 1 {px1} {py1}z'
                p = 'ps1'
            elif pi > rad >= pi * 0.5:  # first quarter to full moon
                if cairo_fix == True:
                    m = 0
                    flag1, flag2 = (1, 1) if darkmode == True else (0, 0)
                else:
                    m = (rad - pi * 0.5) / (pi * 0.5)
                    flag1, flag2 = (0, 0) if darkmode == True else (1, 1)
                px1 = cos(pi * 1.5 - m) * self.r + self.rx
                py1 = sin(pi * 1.5 - m) * self.r + self.ry
                px2 = cos(pi * 1.5 - m) * self.r + self.rx
                py2 = -sin(pi * 1.5 - m) * self.r + self.ry
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 0 {px1} {py1}z'
                p = 'ps2'
            elif pi * 1.5 > rad >= pi:  # full moon to third quarter
                if cairo_fix == True:
                    m = 0
                    flag1, flag2 = (1, 1) if darkmode == True else (0, 0)
                else:
                    m = (pi * 1.5 - rad) / (pi * 0.5)
                    flag1, flag2 = (0, 0) if darkmode == True else (1, 1)
                px1 = cos(pi * 0.5 - m) * self.r + self.rx
                py1 = sin(pi * 0.5 - m) * self.r + self.ry
                px2 = cos(pi * 0.5 - m) * self.r + self.rx
                py2 = -sin(pi * 0.5 - m) * self.r + self.ry
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 0 {px1} {py1}z'
                p = 'ps3'
            else:  # third quarter to new moon
                m = (rad - pi * 1.5) / (pi * 0.5)
                px1 = cos(pi * 0.5 + m) * self.r + self.rx
                py1 = sin(pi * 0.5 + m) * self.r + self.ry
                px2 = cos(pi * 0.5 + m) * self.r + self.rx
                py2 = -sin(pi * 0.5 + m) * self.r + self.ry
                flag1, flag2 = (1, 0) if darkmode == True else (0, 1)
                dm = f'M{px1} {py1} A{ra1} {ra1} 0 {flag1} {flag2} {px2} {py2} {ra2*0.98} {ra3*0.98} 0 1 1 {px1} {py1}z'
                p = 'ps4'
        return dm,p
    
def svg_format(_svg):
    encoding = 'iso-8859-1'
    height = 800
    width = 2400
    svg = f'''<?xml version="1.0" encoding="{encoding}"?>
<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">
{_svg}
</svg>\n'''
    return svg

def main():
    lat = 1
    r = 25
    rx = 75
    ry = 75
    cairo_fix = True
    
    def gen_svg(ps, darkmode, cairo_fix):
        ra1 = 1 * r
        ra3 = 1 * r
        _svg = str()
        style = f'fill:black;stroke:black;stroke-width:1px;'
        for val in range(29):
            rad = val / 29 * pi * 2 if val / 29 < 1 else pi * 2
            ra2 = (cos(rad) * r)
            dm,p = ps.moon(ra1, ra2, ra3, rad, darkmode, cairo_fix) 
            _svg += f'<path d="{dm}" style="{style}"/>\n'
            _svg += f'<circle cx="{ps.rx}" cy="{ps.ry}" r="{ps.r}" stroke="black" stroke-width="1" fill="none"/>\n'
            _svg += f'<text style="text-anchor:middle;" font-size="16px" x="{ps.rx}" y="{ry+50}">{p}</text>\n'
            ps.rx += 75
        return _svg
        
    north_ps = Phase(r, rx, ry, lat)
    ry += 100
    north_ps_dark = Phase(r, rx, ry, lat)
    ry += 100
    south_ps = Phase(r, rx, ry, -lat)
    ry += 100
    south_ps_dark = Phase(r, rx, ry, -lat)
    
    _svg = str()    
    _svg += gen_svg(north_ps,darkmode=False, cairo_fix=cairo_fix)
    _svg += gen_svg(north_ps_dark,darkmode=True, cairo_fix=cairo_fix)
    _svg += gen_svg(south_ps,darkmode=False, cairo_fix=cairo_fix)
    _svg += gen_svg(south_ps_dark,darkmode=True, cairo_fix=cairo_fix)
    svg = svg_format(_svg)
    with open('test_moonphase.svg', 'w') as f:
        f.write(svg)
    svg2png(bytestring=svg,write_to='test_moonphase.png')
main()
