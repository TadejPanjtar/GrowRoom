import RPi.GPIO as GPIO
import am2302_ths as ths
from stgs import stgs

RelayON  = False  # relay are driven inverted
RelayOFF = True
LedON  = False
LedOFF = True
# Wiring
Rlight  = 27 # relay 1 - light
Rpomp   = 22 # relay 2 - pomp
Rheat   = 23 # relay 3 - heat
Rpomp2  = 24 # relay 4 - pomp2
THS     = 25 # temperature humidity sensor
LED1    = 26 # indicating relay1
LED2    = 13 # if temperature too low
LED3    =  5 # if humidity too low
LED4    =  6 # if moisture too low

GPIO.setmode(GPIO.BCM)
GPIO.setup(Rlight, GPIO.OUT)
GPIO.setup(Rheat,  GPIO.OUT)
GPIO.setup(Rpomp,  GPIO.OUT)
GPIO.setup(Rpomp2, GPIO.OUT)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

# turnung OFF defaults
GPIO.setup(Rlight, RelayOFF)
GPIO.setup(Rheat, RelayOFF)
GPIO.setup(Rpomp, RelayOFF)
GPIO.setup(Rpomp2, RelayOFF)
GPIO.setup(LED3, LedOFF)

t=None; h=None;
while not(t): t=ths.get_temperature(THS);

while not(h): h=ths.get_humidity(THS);

if t: # handle empty variable
  temperature=t

if h:
  humidity=h

#print 'temp',temperature, 'hum', humidity
print 'Temp={0:0.1f}*C Humidity={1:0.1f}%' .format(temperature, humidity)

from chirp import Chirp
# chirp = Chirp(1, 0x6f)
# chirp.cap_sense()
