#!/bin/sh

DEBIAN_PATH=/mnt/us/DebianKindle/mnt

ntpdate 192.168.2.1 >/dev/null 2>&1
#chroot $DEBIAN_PATH /bin/bash -c "ntpdate 192.168.2.1 >/dev/null 2>&1"
