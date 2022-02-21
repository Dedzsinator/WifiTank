#!/bin/bash
/usr/local/bin/gpio -g mode 26 out

wget -q --spider http://google.com

while true; do
    if [ $? -eq 0 ]; then
    	/usr/local/bin/gpio -g write 26 0
    	sleep 1
    	/usr/local/bin/gpio -g write 26 1
    	sleep 1
   fi
done
