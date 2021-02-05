#!/usr/bin/python3
import csv
import plotille
import datetime
import sys
import fileinput
import os
import time
"""
papertty h8 w40
pitft h23 w39
"""
width=40
height=10

now = datetime.datetime.now()

y = []
x = []

for line in fileinput.input():
    line = line.split(",")
    print(line)
    if type(line) is list:
        x.append(datetime.datetime.fromtimestamp(int(line[0])))
        y.append(float(line[1].strip()))
    else:
        
        now = datetime.datetime.now()
        y.append(float(line))
        x.append(now)
    if len(x) > 1:
        os.system("clear")
        print(plotille.plot(x[-width:], y[-width:], height=height, width=47, Y_label="ms/T", X_label="t"), end='')
    
