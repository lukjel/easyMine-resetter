import RPi.GPIO as GPIO
import json
import time

comPins = [17, 18, 27, 22, 23, 24, 25, 4]

def pinSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in comPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

def powerOff(compNum):
    GPIO.output(comPins[compNum], 0)
    time.sleep(8)
    GPIO.output(comPins[compNum], 1)

def powerOn(compNum):
    powerOff(compNum)
    time.sleep(0.5)
    GPIO.output(comPins[compNum], 0)
    time.sleep(0.5)
    GPIO.output(comPins[compNum], 1)
