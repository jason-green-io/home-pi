#!/bin/bash

OLD=""
while $(sleep 1); do

LINE0=$(date +%A)
LINE1="$(date +"%Y/%m/%m %H:%M")"
LINE2="$(( ( $(date -d "2021/07/01" +%s) - $(date +%s) ) / (3600 * 24) ))d until Canada day"


NEW="$LINE0\n$LINE1\n$LINE2\n$LINE3"

if [ "$NEW" != "$OLD" ]; then
    clear
    echo -e "$NEW" | toilet -f smblock
    #| /usr/bin/toilet -f smblock -w 62 --gay'
fi

OLD="$NEW"

done
