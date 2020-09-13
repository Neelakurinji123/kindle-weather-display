#!/bin/sh

OUTPUT_DIR=/tmp/www

test -d /tmp/www || mkdir -p /tmp/www
cd "$(dirname "$0")"
/usr/bin/python3 createSVG.py

#convert -size 600x800 -background white -depth 8 \
#    $OUTPUT_DIR/ieroStation.svg $OUTPUT_DIR/kindleStation.png
#
#gm convert -size 600x800 -background white -depth 8 -resize 600x800 \
#    -colorspace gray -type palette -geometry 600x800 \
#    $OUTPUT_DIR/ieroStation.svg $OUTPUT_DIR/kindleStation.png

sleep 3
cd $OUTPUT_DIR; pngcrush -s -c 0 -ow kindleStation.png

