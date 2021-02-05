import colour
import collections
import blinkt
import time
import threading
import os
import socket
import ssl
import json
from blinkt import set_clear_on_exit, set_brightness, set_pixel, show

# clear the Blinkt! on exit
set_clear_on_exit()
# this is plenty bright, these light are super bright
set_brightness(0.1)

# various colors
skyColor = "#000022"
sunsetColor = "#FF4500"
sunriseColor = "#FF4500"
nightColor = "#010101"

# this is what we're using as sunset times in game ticks, taken from the wiki
sunset = (7698, 13805)
sunrise = (22550, 450)

# initial values, these get changed later
moonPhase = 0
serverTime = 12000


def on_connect(client, userdata, flags, rc):
    ''' used by paho, notice we're subscribing to the servertim topic coming from the server '''
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("servertime" , 1 )

    
def on_message(client, userdata, msg):
    '''runs every time paho gets a message '''
    # grab the global objects for the moon and time 
    global serverTime
    global moonPhase
    print("topic: "+ msg.topic)
    print("payload: "+ str(msg.payload))

    # parse it, since the server sends it to us via json
    payload = json.loads(msg.payload.decode("utf-8"))

    # update the values
    serverTime = payload[1]

    moonPhase = divmod(payload[0], 8)[1]



def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]

    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''

    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
        int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
        for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return RGB_list



# here we assemble a list of all the color values for the sky, calculating gradients between the different milstones
# 450 - 7698
day = (7698 - 450) * [hex_to_RGB(skyColor)]
#7698 - 13048
sunsetPart1 = linear_gradient(skyColor, sunsetColor, n=13048 - 7698)
#13048 - 13805
sunsetPart2 = linear_gradient(sunsetColor, nightColor, n=13805 - 13048)
#13805 - 22549
night = (22549 - 13805) * [hex_to_RGB(nightColor)]
# 22549 - 22925
sunrisePart1 = linear_gradient(nightColor, sunriseColor, n=22925 - 22549)
#22925  - 450
sunrisePart2 = linear_gradient(sunriseColor, skyColor, n=24000 - 22925 + 450)

# stick them all together
gradient = collections.deque(day + sunsetPart1 + sunsetPart2 + night + sunrisePart1 + sunrisePart2)

# and rotate them so the index corresponds to the tick
gradient.rotate(450)




def getMoonPixel(time):
    '''  return which pixel the moon is in'''
    moon = (12575, 23459)
    if not (time >= moon[0] and time < moon[1]):
        return None
    else:
        bodyRange = moon[1] - moon[0]
        time = time - moon[0]
        return int(time / float(bodyRange) * 8)


def getSunPixel(time):
    ''' return which pixel the sun is in '''
    sun = (22925, 13048)
    if not (time >= sun[0] or time < sun[1]):
        return None

    else:
        if time < sun[1]:
            
            time += 24000
        bodyRange = sun[1] + 24000 - sun[0]
        time = time - sun[0]

        return int(time / float(bodyRange) * 8)


def display(serverTime, moonPhase):
    '''continually update the display based on the global values of the moon phase and server time'''
    
    
    for x in range(8):

        r, g, b = gradient[serverTime]
        set_pixel(x,r,g,b)

    moonPixel = getMoonPixel(serverTime)
    if moonPixel != None:
        c = abs(4 - moonPhase) / 4 * 255
        set_pixel(moonPixel, c, c, c)

    sunPixel = getSunPixel(serverTime)
    if sunPixel != None:
        set_pixel(sunPixel, 255, 255, 0)

    show()
    time.sleep(0.011)
    #print(each)
    #time.sleep(0.0001)

def genTicks():
    '''  used to generate ticks to test the display '''
    global serverTime
    while True:
        serverTime = divmod(serverTime + 10, 24000)[1]
        print(serverTime)
        time.sleep(0.01)
        
"""
# connect to AWS IoT
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

# if you plan on using this code, you'll need to change this stuff
awshost = "data.iot.eu-west-1.amazonaws.com"
awsport = 8883
clientId = "endermite"
thingName = "endermite"
caPath = "aws-iot-rootCA.crt"
certPath = "8cb2484aa1-certificate.pem.crt"
keyPath = "8cb2484aa1-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)


# start the display
displayThread = threading.Thread(target=display)
displayThread.start()

# for debug purposes
#tickThread = threading.Thread(target=genTicks)
#tickThread.start()


# start getting values from server 
mqttc.loop_forever()
"""


        

