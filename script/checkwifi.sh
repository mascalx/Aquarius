#!/bin/bash

# Instructions:
#
# o Install where you want to run it from like /usr/local/bin
# o chmod 0755 /usr/local/bin/checkwifi.sh
# o Add to crontab
#
# Run Every 5 mins - Seems like ever min is over kill unless
# this is a very common problem.  If once a min change */5 to *
# once every 2 mins */5 to */2 ... 
#
# */5 * * * * /usr/local/bin/checkwifi.sh

if ifconfig wlan0 | grep -q "inet addr:" ; then
   echo "wlan is connected"
else
   ifup --force wlan0
fi
