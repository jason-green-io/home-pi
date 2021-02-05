#!/bin/bash
VAR=($(stty size))
for i in $(eval echo "{1..${VAR[0]}}")
do
  echo -ne "\n"
done
clear
