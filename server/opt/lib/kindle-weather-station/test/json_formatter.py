#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import json
import sys

file = sys.argv[1]
with open(file, 'r') as f:
    a = json.load(f)
            
output = file.split('.')[0] + '_formatted.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump(a, f, ensure_ascii=False, indent=4)
