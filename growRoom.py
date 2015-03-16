import RPi.GPIO as GPIO
import am2302_ths as ths

from time import strftime,sleep
from stgs import stgs


lightHours=[]
lightOldOn=False # read light status
LIGHT_HOURS_LEAP=24
LIGTH_HOURS_START=stgs.lightStart
LIGTH_HOURS_DURATION=stgs.lightDuration
tenMinutesRun=False
blinkTick=0
temperature=0
humidity=0
moisture=0
LOGGING=True

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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
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
  if temperature<stgs.temperature:
    GPIO.setup(Rheat, RelayON)
    log("Heating ON")
  else:
    GPIO.setup(Rheat, RelayOFF)
    log("Heating OFF")
   
def handle_pomp():
  if humidity<stgs.humidity:
    GPIO.setup(Rpomp, RelayON)
    sleep(10)
    GPIO.setup(Rpomp, RelayOFF)
    log("Spraying")

def tenMinutesCheck():
  global tenMinutesRun, blinkTick
  tenMinutes=(strftime("%S")[1]=='0') # every 10 minutes
  if tenMinutesRun!=tenMinutes:
    print "10 minutes"
    if tenMinutes: 
      handle_light()
      handle_heating()
      handle_pomp()
    #  handle_pomp2()
    blinkTick=0
  tenMinutesRun=tenMinutes

t=None; h=None; moisture=33;

while True:
  if blinkTick % 3 == 0:
    t=ths.get_temperature(THS);
    if t: # handle empty variable
      temperature=t;
  if blinkTick % 3 == 1:
    h=ths.get_humidity(THS); 
    if h:
      humidity=h;
  if blinkTick % 3 == 2:
    # print "sensor 3" # TODO implement
    sleep(1)
  if blinkTick % 2== 0:
    if temperature<stgs.temperature:
      GPIO.setup(LED2, LedON)
    if humidity<stgs.humidity:
      GPIO.setup(LED3, LedON)
    if moisture<stgs.moisture:
      GPIO.setup(LED4, LedON)
    log('Temp={0:0.1f}*C Humidity={1:0.1f}% Moisture={2:4d}%' .format(temperature, humidity, moisture))
  else:
    GPIO.setup(LED2, LedOFF)
    GPIO.setup(LED3, LedOFF)
    GPIO.setup(LED4, LedOFF)
  blinkTick=blinkTick+1
  tenMinutesCheck()
   

from chirp import Chirp
# chirp = Chirp(1, 0x6f)
# chirp.cap_sense()
