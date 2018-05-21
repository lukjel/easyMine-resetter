import RPi.GPIO as GPIO
import json
import time
import os

portPins = [17, 18, 27, 22, 23, 24, 25, 4]

def pinSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in portPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

def powerOff(portNum):
    GPIO.output(portPins[portNum], 0)
    time.sleep(8)
    GPIO.output(portPins[portNum], 1)

def powerOn(portNum):
    powerOff(portNum)
    time.sleep(0.5)
    GPIO.output(portPins[portNum], 0)
    time.sleep(0.5)
    GPIO.output(portPins[portNum], 1)

def reset(portNum):
    GPIO.output(portPins[portNum], 0)
    time.sleep(0.5)
    GPIO.output(portPins[portNum], 1)

def restart(portNum):
    os.system('shutdown -r now')

cmdEnum = {
    'device-power-on': powerOn,
    'device-power-off': powerOff,
    'device-restart': reset,
    'controller-upgrade': restart
}

def cmdHandler(cmdId, cmdName, cmdPort):
    if cmdName in cmdEnum:
        cmdEnum[cmdName](cmdPort)
        return 0
    return 1
