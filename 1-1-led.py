import RPi. GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
import RPi. GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
state=0
period = 1.0
while True:
    GPIO.output(led, state)
    state = not state
    time.sleep(period)