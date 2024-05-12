#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import json
import sys

file = sys.argv[1] if len(sys.argv) >= 3 else None
if len(sys.argv) < 3:
    print("usage:", sys.argv[0], "jsonfile", "key1", "[key2]", "[ key3]")
    exit(0)
elif len(sys.argv) == 3:
    key1 = sys.argv[2]
elif len(sys.argv) == 4:
    key1 = sys.argv[2]
    key2 = sys.argv[3]
elif len(sys.argv) == 5:
    key1 = sys.argv[2]
    key2 = sys.argv[3]
    key3 = sys.argv[4]


with open(file, 'r') as f:
    if len(sys.argv) == 3:
        d = json.load(f)[key1]
        print(d)
    elif len(sys.argv) == 4:
        d = json.load(f)[key1][key2]
        print(d)
    elif len(sys.argv) == 5:
        d = json.load(f)[key1][key2][key3]
        print(d)
