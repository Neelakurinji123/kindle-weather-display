#!/bin/sh

#cd "$(dirname "$0")"
#test -f /tmp/kindleStation.png || eips -g images/error.png

pidof powerd >/dev/null
if [ $? -eq 0 ]; then
    /etc/init.d/powerd stop
    /etc/init.d/framework stop
fi

rm -f /tmp/kindleStation.png
wget -q http://192.168.2.1:8080/kindleStation.png -O /tmp/kindleStation.png
eips -c
eips -g /tmp/kindleStation.png
