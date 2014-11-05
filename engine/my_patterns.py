from PatternObjects import *
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

###############################
##
## Warning!!!!!!!!!
## You must give your functions differnt names
## Overloaded functions will not register properly
##
###############################

#sock = socket(AF_INET, SOCK_STREAM)
#sock.connect(("192.168.1.2", 9000))

def build_x10():
    try:
        x10_sock = socket(AF_INET, SOCK_STREAM)
        x10_sock.connect(("NAS", 5000))
    except Exception as e:
        print e
        sleep(10)
        x10_sock = None
    return x10_sock

"""
@BasePattern.register(gesture = YIncrease((0,15),(70,80),100))
@BasePattern.register(ttl = 500)
def takeoff():
    print "Are you a bad enough dude to program a power glove?"
    #sock.send("takeoff")

@BasePattern.register(gesture = FingerGesture(*[1,0,1,1]))
@BasePattern.register( XDecrease((70,80),(0,20),100))
@BasePattern.register(ttl = 500def land():
    print "LANDING"
    #sock.send("land")
"""

@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(ttl = 100)
def testing():
    print "test complete!"
    sleep(5)

###################################
# X10 functions
@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = YIncrease((0,50),(90,100),100))
@BasePattern.register(ttl = 100)
def lamp1_on():
    print "Turning on"
    x10_sock = build_x10()
    if x10_sock is not None:
        x10_sock.send("--on=1")

@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,0,0,50))
@BasePattern.register(gesture = YDecrease((50,100),(0,10),100))
@BasePattern.register(ttl = 100)
def lamp1_off():
    print "Turning off"
    x10_sock = build_x10()
    if x10_sock is not None:
        x10_sock.send("--off=1")

@BasePattern.register(gesture = FingerGesture(0,1,1,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,1,0,50))
@BasePattern.register(gesture = YIncrease((0,50),(90,100),100))
@BasePattern.register(ttl = 100)
def lamp2_on():
    print "Turning on"
    x10_sock = build_x10()
    if x10_sock is not None:
        x10_sock.send("--on=2")

@BasePattern.register(gesture = FingerGesture(0,1,1,0,50))
@BasePattern.register(gesture = FingerGesture(0,1,1,0,50))
@BasePattern.register(gesture = YDecrease((50,100),(0,10),100))
@BasePattern.register(ttl = 100)
def lamp2_off():
    print "Turning off"
    x10_sock = build_x10()
    if x10_sock is not None:
        x10_sock.send("--off=2")
