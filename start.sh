#!/bin/bash
export PATH=$PATH:/usr:/usr/bin
sleep 30
date
cd /home/pi/home-pi
/usr/bin/tmux new-session -d -s tty || echo already session 

#/usr/bin/tmux new-window -n "PaperTTY" -t tty:11 '/home/pi/PaperTTY/go.sh'
sleep 60
TMUXPTY="$(/usr/bin/tmux list-client | /bin/grep 62x15 | /usr/bin/cut -d: -f1)"
echo $TMUXPTY

# /usr/bin/tmux new-window -n "weather" -t tty:1 '/home/pi/weather2.sh'
/usr/bin/tmux new-window -t tty:4 \; \
	split-window -h \; \
	select-pane -t tty:4.1 \; \
	send-keys './time.sh' C-m \; \
	select-pane -t tty:4.0 \; \
	send-keys './trivia2.sh' C-m \;

# /usr/bin/tmux new-window -n "news" -t tty:2 '/home/pi/news.sh'
# /usr/bin/tmux new-window -n "til" -t tty:3 '/home/pi/til.sh'
# /usr/bin/tmux new-window -n "trivia" -t tty:5 '/home/pi/trivia2.sh'
/usr/bin/tmux new-window -n "controller" -t tty:13 "/home/pi/home-pi/simpleController.py $TMUXPTY"
/usr/bin/tmux new-window -n "lights" -t tty:12 '/usr/bin/gunicorn3 -b :8000 ifttt:__hug_wsgi__'
# /usr/bin/tmux new-window -n "homebridge" -t tty:14 '/usr/local/bin/homebridge'
#/usr/bin/tmux new-window -n "console1" -t tty:14 'sudo stty -F /dev/tty1 cols 74 rows 14; TERM=vt220 sudo conspy -v 1'
