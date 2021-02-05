#!/bin/bash
while true; do
	curl -sA "pi:com.tesseract.endermite:v1 (by /u/greener_ca)"  https://www.reddit.com/r/todayilearned.json | jq -r '.data.children[] | "↑ " + (.data.ups | tostring ) + " -- " + .data.title | tostring' | fold -w 62 -s | timeout --foreground 600 less -M -R -p "↑ [0-9]*|$"
sleep 1
done
reset

