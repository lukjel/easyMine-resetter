import RPi.GPIO as GPIO
import time
import json
import threading

comPins = [17, 18, 27, 22, 23, 24, 25, 4]

def pinSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in comPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

def powerOff(compNum):
    GPIO.output(compNum, 0)
    time.sleep(8)
    GPIO.output(compNum, 1)


def powerOn(compNum):
    powerOff(compNum)
    time.sleep(0.5)
    GPIO.output(compNum, 0)
    time.sleep(0.5)
    GPIO.output(compNum, 1)

# def setup():
#     instructionJson = json.load(open('data.json'))
#     for compNum in instructionJson["turnOn"]:
#         turnOn(comPins[compNum-1])
#     for compNum in instructionJson["turnOff"]:
#         turnOff(comPins[compNum-1])
#     for compNum in instructionJson["turnHardOff"]:
#         turnHardOff(comPins[compNum-1])
#     threading.Timer(10.0, setup).start()
