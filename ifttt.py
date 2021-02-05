#!/usr/bin/python3
'''Endermite rest interface'''
import hug
import sys
import gradient
import hue

@hug.post('/mctime', examples="serverTime=TIME&moonPhase=PHASE")
def mctime(serverTime: hug.types.decimal, moonPhase: hug.types.decimal):
    '''set the BlinkIt to the sky color based on the server time and moon phase'''
    gradient.display(int(serverTime), int(moonPhase))
    print(serverTime, moonPhase)

    return "set server time to {serverTime} and moon phase to {moonPhase}".format(**locals())

@hug.cli()
@hug.get('/lights/start', examples="rooms=ROOMS&holiday=HOLIDAY&speed=1")
def lightsStart(rooms: hug.types.delimited_list(","), holiday: hug.types.text, speed):
    '''set the Hue bulbs to rotate through holiday appropriate colors'''
    print(rooms, holiday, speed)
    hue.ctrl.start((rooms, holiday, speed))


    return("{} {}".format(rooms, holiday, speed))
@hug.cli()
@hug.get('/lights/stop')
def lightsStop():
    print("stopped")
    hue.ctrl.stop()


if __name__ == "__main__":
    __hug__.cli()
