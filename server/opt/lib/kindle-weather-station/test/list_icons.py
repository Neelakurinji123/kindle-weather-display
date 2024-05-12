#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import re
import sys
sys.path.append('..')

import Icons
import IconExtras

icons_set = ['Icons', 'IconExtras']
svgfile = "list_icons.svg"

t_size = [ 150, 150]
col = 4

#l = [ re.sub(r'^__\w*', '', a) for a in dir(Icons) if not re.match ]
l = [ a for a in dir(Icons) if not re.match(r'^__\w*', a)]
print(eval("Icons." + l[0] + "()"))
print(Icons.ClearDay(),  l)

x, y = 0, 0
