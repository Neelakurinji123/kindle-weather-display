#!/bin/sh

#cd "$(dirname "$0")"

pidof powerd >/dev/null
if [ $? -eq 0 ]; then
    /etc/init.d/powerd stop
    /etc/init.d/framework stop
fi

DEBIAN_PATH=/mnt/us/DebianKindle/mnt

rm -f /www/ieroStation.svg
wget -q http://192.168.2.1:8080/ieroStation.svg -O /www/ieroStation.svg
chroot $DEBIAN_PATH /bin/bash -c "convert -background white -depth 8 /var/tmp/ieroStation.svg /var/tmp/kindleStation.png"
chroot $DEBIAN_PATH /bin/bash -c "pngcrush -s -c 0 -ow /var/tmp/kindleStation.png"

eips -c
eips -g /www/kindleStation.png
