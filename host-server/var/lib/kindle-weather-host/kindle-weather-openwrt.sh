#!/bin/sh

test -d /tmp/www || mkdir -p /tmp/www

cd "$(dirname "$0")"
/usr/bin/python3 createSVG.py
