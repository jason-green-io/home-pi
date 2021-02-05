#!/bin/bash

while true; do
curl -s wttr.in/?n | timeout --foreground 1800 less -RS
sleep 1
done
reset
