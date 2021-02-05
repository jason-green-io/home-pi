#!/usr/bin/python3
import buttonshim
import signal
import subprocess
import sys
import threading
import time
import random

tmux = "/usr/bin/tmux"
tmuxPty = "tty"

Rcolor = [0, 64, 128, 192, 255]
Gcolor = [0, 64, 128, 192, 255]
Bcolor = [0, 64, 128, 192, 255]


@buttonshim.on_press(buttonshim.BUTTON_A)
def A(button, pressed):
    subprocess.Popen([tmux, "previous-window", "-t", tmuxPty],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_press(buttonshim.BUTTON_B)
def B(button, pressed):
    subprocess.Popen([tmux, "next-window", "-t", tmuxPty],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=2)
def Erandom(button):
    global Rcolor
    buttonshim.set_pixel(random.choice(Rcolor), Gcolor[0], Bcolor[0])

@buttonshim.on_press(buttonshim.BUTTON_E)
def E(button, pressed):
    global Rcolor
    Rcolor = Rcolor[1:] + Rcolor[:1]
    buttonshim.set_pixel(Rcolor[0], Gcolor[0], Bcolor[0])

@buttonshim.on_press(buttonshim.BUTTON_D)
def D(button, pressed):
    global Gcolor
    Gcolor = Gcolor[1:] + Gcolor[:1]
    buttonshim.set_pixel(Rcolor[0], Gcolor[0], Bcolor[0])


@buttonshim.on_press(buttonshim.BUTTON_C)
def C(button, pressed):
    global Bcolor
    Bcolor = Bcolor[1:] + Bcolor[:1]
    buttonshim.set_pixel(Rcolor[0], Gcolor[0], Bcolor[0])

signal.pause()
