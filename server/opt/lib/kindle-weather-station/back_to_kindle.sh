#!/bin/sh

IP='192.168.2.2'

p=`ssh root@${IP} 'pidof powerd'` 
if [ "$p" == '' ]; then
    ssh root@${IP} '/etc/init.d/powerd start'
    ssh root@${IP} '/etc/init.d/framework start'
fi
