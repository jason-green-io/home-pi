#!/bin/bash
tail -n 100 -f ~/temp.log | awk -F, -W interactive '{print $2}' | ~/plot/plot.py
