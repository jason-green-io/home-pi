#!/usr/bin/python3
import buttonshim
import signal
import subprocess
import sys
import threading
import time

tmuxPty = sys.argv[1]
print(tmuxPty)


tmux = "/usr/bin/tmux"

'''
Button E cycles mode

Mode 0: auto scroll
    A: status bar toggle
    D: scrub display

Mode 1: Nav
    A: PgUp
    B: PgDown
    C: left
    D: right

Mode 2: window choose
    A: choose tree
    B: Up
    C: Down
    D: Enter
'''

modes = [1, 2, 0]
modeColors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255)]
buttonshim.set_pixel(*modeColors[modes[0]])

def cycle():
    global modes
    windows = list(range(1, 6))
    print("Starting cycle thread")
    while True:
        if modes[0] == 0:
            print("Switching to {}".format(windows[0]))
            subprocess.Popen([tmux, "select-window", "-t", "tty:{}".format(windows[0])],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            windows = windows[1:] + windows[:1]
        else:
           print("Not switching")
        time.sleep(30)

cycleThread = threading.Thread(target=cycle)
cycleThread.start()




@buttonshim.on_press(buttonshim.BUTTON_A)
def A(button, pressed):
    if modes[0] == 1:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "PgUp"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 2:
        subprocess.Popen([tmux, "choose-tree", "-t", tmuxPty, "-u"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 0:
        subprocess.Popen([tmux, "set-option", "-t", tmuxPty, "status"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_press(buttonshim.BUTTON_B)
def B(button, pressed):
    if modes[0] == 1:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "PgDn"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 2:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "Up"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_press(buttonshim.BUTTON_C)
def C(button, pressed):
    if modes[0] == 1:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "Left"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 2:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "Down"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_press(buttonshim.BUTTON_D)
def D(button, pressed):
    if modes[0] == 1:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "Right"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 2:
        subprocess.Popen([tmux, "send-keys", "-t", tmuxPty, "Enter"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elif modes[0] == 0:
        subprocess.Popen(["pkill", "-f", "papertty", "-USR1"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_press(buttonshim.BUTTON_E)
def modeChange(button, pressed):
    global modes, modeColors
    modes = modes[1:] + modes[:1]
    buttonshim.set_pixel(*modeColors[modes[0]])
    print(modes)

signal.pause()
