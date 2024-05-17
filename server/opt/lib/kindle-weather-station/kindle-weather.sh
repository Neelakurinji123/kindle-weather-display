#!/bin/sh

IP='192.168.2.2'
PNGfile='KindleStation_flatten.png'

# Kindle's daemons stop
p=`ssh root@${IP} 'pidof powerd'` 
if [ "$p" != '' ]; then
    ssh root@${IP} "/etc/init.d/powerd stop"
    ssh root@${IP} "/etc/init.d/framework stop"
fi

cd "$(dirname "$0")"
/usr/bin/python3 CreateSVG.py $1
sleep 3
scp /tmp/$PNGfile root@${IP}:/tmp
ssh root@${IP} "cd /tmp; /usr/sbin/eips -c"
ssh root@${IP} "cd /tmp; /usr/sbin/eips -g $PNGfile"
