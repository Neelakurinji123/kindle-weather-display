#!/bin/sh

cd "$(dirname "$0")"

#test -f /www/kindleStation.png || eips -g images/error.png

if [ -f /mnt/us/kindle-weather/enable ]; then

    if [ "`pidof powerd`" != '' ]; then
        /etc/init.d/powerd stop
        /etc/init.d/framework stop
    fi

    if [ "`mount -l | grep 'tmpfs on /www'`" == '' ]; then
        mount -a
        sleep 3
    fi

    rm -f /www/kindleStation.png
    wget -q http://192.168.2.1:8080/kindleStation.png -O /www/kindleStation.png
    eips -c
    eips -g /www/kindleStation.png
fi
