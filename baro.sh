#!/bin/bash

while true;
do
	NOW=$(date +%s)
	BARO=$(rsstail -d -1 -u https://weather.gc.ca/rss/city/on-118_e.xml | grep Pressure | sed -e 's/<b>Pressure \/ Tendency:<\/b> \(.*\) kPa .*$/\1/')
	echo "$NOW,$BARO"
	sleep 1800
done
