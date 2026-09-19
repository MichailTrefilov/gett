import RPi. GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led,GPIO.OUT)
photo=6
GPIO.setup(photo,GPIO.IN)
while True:
    photos= GPIO.input(photo)
    photos=not photos
    GPIO.output(led, photos)