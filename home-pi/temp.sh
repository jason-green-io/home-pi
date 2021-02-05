#!/bin/bash

while true;
do
	TEMP=$(rsstail -1 -u https://weather.gc.ca/rss/city/on-118_e.xml | grep Current | sed -e 's/.* \(.*\)°C$/\1/')
	NOW=$(date +%s)
	#echo "$NOW,$TEMP"
	echo "$TEMP"
	sleep 1800
done
