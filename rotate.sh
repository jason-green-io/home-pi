#!/bin/bash
while true; do 
	for w in {0..2}; do 
		tmux select-window -t tty:$w
		sleep 30
	done
done
