#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

# Reguler font
class text:
    def __init__(self, anchor, fontsize, x, y, v, stroke=None):
        self.anchor = anchor
        self.fontsize = fontsize
        self.x = x
        self.y = y
        self.v = v
        self.stroke = stroke

    def svg(self):
        if not self.stroke == None:
            return f'<text style="text-anchor:{self.anchor};" font-size="{self.fontsize}px" x="{self.x}" y="{self.y}" stroke="{self.stroke}" fill="{self.stroke}">{self.v}</text>\n'
        else:
            return f'<text style="text-anchor:{self.anchor};" font-size="{self.fontsize}px" x="{self.x}" y="{self.y}">{self.v}</text>\n'
# Bold font
class text2:
    def __init__(self, anchor, fontweight, fontsize, x, y, v):
        self.anchor = anchor
        self.fontweight = fontweight
        self.fontsize = fontsize
        self.x = x
        self.y = y
        self.v = v

    def svg(self):
        return f'<text style="text-anchor:{self.anchor};" font-weight="{self.fontweight}" font-size="{self.fontsize}px" x="{self.x}" y="{self.y}">{self.v}</text>\n'

class circle:
    def __init__(self, cx, cy, r, stroke, width, fill):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.stroke = stroke
        self.width = width
        self.fill = fill

    def svg(self):
        return f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.r}" stroke="{self.stroke}" stroke-width="{self.width}" fill="{self.fill}"/>\n'
        
class line:
    def __init__(self, x1, x2, y1, y2, style):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.style = style

    def svg(self):
        return f'<line x1="{self.x1}" x2="{self.x2}" y1="{self.y1}" y2="{self.y2}" style="{self.style}"/>\n'

class transform:
    def __init__(self, matrix, obj):
        self.matrix = matrix
        self.obj = obj

    def svg(self):
        return f'<g transform="matrix{self.matrix}">{self.obj}</g>\n'


class polyline:
    def __init__(self, points, style):
        self.points = points
        self.style = style

    def svg(self):
        return f'<polyline points="{self.points}" style="{self.style}"/>\n'


class rect:
    def __init__(self, x, y, width, height, style):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style

    def svg(self):
        return f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" style="{self.style}"/>\n'


class path:
    def __init__(self, d, style):
        self.d = d
        self.style = style

    def svg(self):
        return f'<path d="{self.d}" style="{self.style}"/>\n'
        
class spline:
    #/* bezier-spline.js
    # *
    # * computes cubic bezier coefficients to generate a smooth
    # * line through specified points. couples with SVG graphics 
    # * for interactive processing.
    # *
    # * For more info see:
    # * http://www.particleincell.com/2012/bezier-splines/ 
    # *
    # * Lubos Brieda, Particle In Cell Consulting LLC, 2012
    # * you may freely use this algorithm in your codes however where feasible
    # * please include a link/reference to the source article
    # */
    #
    #  Translated from javascript to python by krishna@hottnalabs.net
    #
    #
    #def __init__(self, lst, stroke=1, stroke_color='black', fill='none'):
    #def __init__(self, lst, stroke='black', stroke_color='black', fill='none'):
    def __init__(self, lst, _x=None, _y=None, stroke='black', stroke_width=5, stroke_linecap='round', fill='none'):
        self.lst = lst
        self._x = _x
        self._y = _y
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_linecap = stroke_linecap
        self.fill = fill
        
    def calc(self, _lst):
        n = len(_lst) - 1
        p1 = [ None for _ in range(n)]
        p2 = [ None for _ in range(n)]
        a = [ None for _ in range(n)]
        b = [ None for _ in range(n)]
        c = [ None for _ in range(n)]
        r = [ None for _ in range(n)]
        # left most segment
        a[0] = 0
        b[0] = 2
        c[0] = 1
        r[0] = _lst[0] + 2 * _lst[1]
        # internal segment
        for i in range(1, n-1):
            a[i] = 1
            b[i] = 4
            c[i] = 1
            r[i] = 4 * _lst[i] + 2 * _lst[i+1]
        # right segment
        a[n-1] = 2
        b[n-1] = 7
        c[n-1] = 0
        r[n-1] = 8 * _lst[n-1] + _lst[n]
        # solves Ax=b with the Thomas algorithm (from Wikipedia)
        for i in range(1, n):
            m = a[i] / b[i-1]
            b[i] = b[i] - m * c[i-1]
            r[i] = r[i] - m * r[i-1]
        p1[n-1] = r[n-1] / b[n-1]
        for i in range(n-2, -1, -1):
            p1[i] = (r[i] - c[i] * p1[i+1]) / b[i]
        # we have p1, now compute p2
        for i in range(0, n-1):
            p2[i] = 2 * _lst[i+1] - p1[i+1]
        p2[n-1] = 0.5 * (_lst[n] + p1[n-1])
        return p1, p2
        
    def svg(self):
        x = [s[0] for s in self.lst]
        y = [s[1] for s in self.lst]
        px_p1, px_p2 = self.calc(x)
        py_p1, py_p2 = self.calc(y)
        n = len(self.lst) - 1
        a = list()
        for i in range(n):
            a += [f'{x[i]} {y[i]} C {px_p1[i]} {py_p1[i]} {px_p2[i]} {py_p2[i]}']
        a += [f'{x[n]} {y[n]}']
        if self._x == None and self._y == None:
            svg = '<path d="M ' + ' '.join(a) + f'" stroke="{self.stroke}" stroke-width="{self.stroke_width}" stroke-linecap="{self.stroke_linecap}" fill="{self.fill}"/>'
            #svg = '<path d="M ' + ' '.join(a) + f'" stroke="{self.stroke}" stroke-width="{self.stroke_width}" stroke-linecap={self.stroke_linecap} fill="{self.fill}"/>'

        else:
            _a = ' '.join(a)
            end_x = x[-1]
            svg = f'<path d="M {self._x} {self._y} L {_a} L {end_x} {self._y} Z" stroke="{self.stroke}" stroke-width="{self.stroke_width}" stroke-linecap="{self.stroke_linecap}" fill="{self.fill}"/>'
        return svg
        
