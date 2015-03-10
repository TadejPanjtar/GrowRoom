import RPi.GPIO as GPIO


ReleON  = False
ReleOFF = True
Rlight  = 27 # rele 1 - light

GPIO.setmode(GPIO.BCM)
GPIO.setup(Rlight, GPIO.OUT)
#GPIO.setup(Rlight, ReleOFF)
