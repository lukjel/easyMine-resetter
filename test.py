import RPi.GPIO as GPIO
import time

def pinSetup(pinNo):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinNo, GPIO.OUT)
    GPIO.output(pinNo, 1)

def doPin(pinNo):
    GPIO.output(pinNo, 0)
    time.sleep(1)
    GPIO.output(pinNo, 1)
    time.sleep(1)
    GPIO.output(pinNo, 0)
    time.sleep(1)
    GPIO.output(pinNo, 1)

try:
    print('Starting...')
    pinSetup(0)
    print('Test')
    doPin(0)

except Exception as e:
    print('Error:')
    print(e)
