#!/usr/bin/env python
import RPi.GPIO as GPIO
import am2302_ths as ths

from time import strftime,sleep
from stgs import stgs


lightHours=[]
lightOldOn=False # read light status
NumSensors = 3
LIGHT_HOURS_LEAP=24
LIGTH_HOURS_START=stgs.lightStart
LIGTH_HOURS_DURATION=stgs.lightDuration
tenMinutesRun=False
blinkTick=0
temperature=0
humidity=0
moisture=0
LOGGING=True
heating=False

def log(msg):
  if LOGGING:  print strftime("%Y-%m-%d %X"), msg

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
MOIST   = 17 # moisture digital input

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(MOIST,  GPIO.IN)

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

if (LIGTH_HOURS_START+LIGTH_HOURS_DURATION > LIGHT_HOURS_LEAP):
  lightHours = range(LIGTH_HOURS_START,LIGHT_HOURS_LEAP) + range(0, LIGTH_HOURS_START+LIGTH_HOURS_DURATION-LIGHT_HOURS_LEAP)
else:
  lightHours = range(LIGTH_HOURS_START, LIGTH_HOURS_START+LIGTH_HOURS_DURATION)

def handle_light():
  global lightOldOn
  currentHour=int(strftime("%S")) #int(strftime("%H"))
  lightOn=True if currentHour in lightHours else False
  if lightOldOn!=lightOn:
    s=' OFF '
    if lightOn==True: s=' ON '
    log('Turning lights'+s)
    if lightOn:
      GPIO.setup(Rlight, RelayON)
      GPIO.setup(LED1, LedON)
    else:
      GPIO.setup(Rlight, RelayOFF)
      GPIO.setup(LED1, LedOFF)
  lightOldOn=lightOn

print 'lightHours', lightHours

def handle_heating():
  global heating
  h=temperature<stgs.temperature
  if heating!=h:
    if h:
      GPIO.setup(Rheat, RelayON)
      log("Heating ON")
    else:
      GPIO.setup(Rheat, RelayOFF)
      log("Heating OFF")
  heating=h

def handle_pomp():
  if humidity<stgs.humidity:
    GPIO.setup(Rpomp, RelayON)
    log("Spraying")
    sleep(stgs.pomp1duration)
    GPIO.setup(Rpomp, RelayOFF)

def handle_pomp2():
  if not(moisture):
    GPIO.setup(Rpomp2, RelayON)
    log("Watering")
    sleep(stgs.pomp2duration)
    GPIO.setup(Rpomp2, RelayOFF)

def tenMinutesCheck():
  global tenMinutesRun, blinkTick
  tenMinutes=(strftime("%M")[1]=='0') # every 10 minutes
  if tenMinutesRun!=tenMinutes:
    if tenMinutes: 
      handle_light()
      handle_heating()
      handle_pomp()
      handle_pomp2()
    blinkTick=0
  tenMinutesRun=tenMinutes

t=None; h=None; moisture=False;

while True: # Main loop end
  if blinkTick % NumSensors == 0:
    t=ths.get_temperature(THS);
    if t: # handle empty variable
      temperature=t;
  if blinkTick % NumSensors == 1:
    h=ths.get_humidity(THS); 
    if h:
      humidity=h;
  if blinkTick % NumSensors == 2:
    moisture = (GPIO.input(MOIST) == GPIO.LOW)
    sleep(1)
  if blinkTick % 2== 0: #every second tick conditionally turns leds on to blink
    if temperature<stgs.temperature:
      GPIO.setup(LED2, LedON)
    if humidity<stgs.humidity:
      GPIO.setup(LED3, LedON)
    if not(moisture):
      GPIO.setup(LED4, LedON)
    log('Temp={0:0.1f}*C Humidity={1:0.1f}% Moisture={2}' .format(temperature, humidity, moisture))
  else: #turn leds off
    GPIO.setup(LED2, LedOFF)
    GPIO.setup(LED3, LedOFF)
    GPIO.setup(LED4, LedOFF)
  blinkTick=blinkTick+1
  tenMinutesCheck()
  # Main loop end

from chirp import Chirp
# chirp = Chirp(1, 0x6f)
# chirp.cap_sense()
