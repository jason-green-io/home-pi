#!/bin/bash


while true; do
rsstail -1 -u https://weather.gc.ca/rss/city/on-118_e.xml -d -H -N | fold -w 62 -s | timeout --foreground 600 less -M -R -p "[0-9]* cm|[Ff]reezing rain|[Ss]now|Sunday:|Monday:|Tuesday:|Wednesday:|Thursday:|Friday:|Saturday:|night:"
sleep 1
done
reset
