import RPi.GPIO as GPIO
import am2302_ths as ths

RelayON  = False  # relay are driven inverted
RelayOFF = True

# Wiring
Rlight  = 27 # relay 1 - light
Rpomp   = 22 # relay 2 - pomp
Rheat   = 23 # relay 3 - heat
Rpomp2  = 24 # relay 4 - pomp2
THS     = 25 # temperature humidity sensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(Rlight, GPIO.OUT)
#GPIO.setup(Rlight, RelayOFF)

t=None; h=None;
while not(t): t=ths.get_temperature(THS);
while not(h): h=ths.get_humidity(THS);
if t: # handle empty variable
  temperature=t
if h:
  humidity=h
#print 'temp',temperature, 'hum', humidity
print 'Temp={0:0.1f}*C Humidity={1:0.1f}%' .format(temperature, humidity)


