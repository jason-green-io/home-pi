from phue import Bridge
import itertools
import time
import rgbxy
import collections
from rgbxy import Converter
from rgbxy import GamutB # or GamutB, GamutC
import random
import threading

running = True

converter = Converter(GamutB)

red = converter.hex_to_xy('ff0000')
white = converter.hex_to_xy('ffffff')
green = converter.hex_to_xy('00ff00')
purple = converter.hex_to_xy("8B008B")
orange = converter.hex_to_xy("FF8C00")
yellow = converter.hex_to_xy("ffff00")
blue = converter.hex_to_xy("0000ff")

colorsDict = {
    "halloween": [orange, red, purple],
    "christmas": [red, green, blue, yellow, orange]
    
}

d = collections.deque([red, green, white, green, red, green, white, green])


# RGWGRGWG


b = Bridge('192.168.7.36')
b.connect()
b.get_api()

lightsDict = {
    "outside": ["Front entrance", "Front Door", "Garage Door"],
    "tvroom": ["TV front right", "TV front left", "TV back left", "TV back right"],
    "dining": ["Dining1", "Dining2", "Dining3", "Dining4", "Dining5", "Dining6", "Dining7", "Dining8",],
    "hallway": ["Hallway"],
    "large": ["Large1", "Large2", "Large3"],
    "medium": ["Medium1", "Medium2", "Medium3"],
    "small": ["Small1", "Small2", "Small3"]
}


#prevlight = lights[-1]
def rotate():
    [b.set_light(l, "on", True) for l in lights]
    
    while 1:
    #b.set_light(prevlight, "on", False)
        for light in zip(lights, d):
            print(light)
            b.set_light(light[0], "xy", light[1], transitiontime=0)
            time.sleep(1)        
    
    
    
            #prevlight = light
    
        d.rotate(1)


class randoControl():
    running = True
    t = ''
    def __init__(self):
        print("Init controller")
    
    def rando(self, lights, colors, speed):
        lightsOn = []
        for each in lights:
            lightsOn.extend(lightsDict.get(each, []))
            colorsOn = colorsDict.get(colors, [red])
            print(lightsOn,colorsOn)
        self.running = True
        while self.running:
            b.set_light(random.choice(lightsOn), "xy",random.choice(colorsOn),transitiontime=20)
            time.sleep(float(speed) / len(lightsOn))
        print("stopped")



    def start(self, args):

        print("Starting thread with", args)
        if not self.t or not self.t.is_alive():
            
            self.t = threading.Thread(target=self.rando, args=args, daemon=True)
            self.t.start()
        else:
            print("already started")

    def stop(self):
        self.running = False



ctrl = randoControl()
