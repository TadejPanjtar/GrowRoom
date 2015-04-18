#!/usr/bin/env python
import RPi.GPIO as GPIO
import am2302_ths as ths
import os
from time import strftime,sleep
from stgs import stgs

current_dir = os.path.dirname(os.path.abspath(__file__))
NumSensors = 3
lightOldOn=False # read light status
LIGHT_HOURS_LEAP=24
tenMinutesRun=False
blinkTick=0
temperature=0
humidity=0
moisture=0
LOGGING=True
logs=[]
LOGS_SIZE=55
heating=False

def log(msg):
  # if LOGGING:  print strftime("%Y-%m-%d %X"), msg
    if LOGGING:
      logs.append(strftime("%d-%X")+" "+ msg)
      if (len(logs)>LOGS_SIZE): del logs[0]

def gv(v): # get value var. or atribute US: gv('c.sub.s.a') --> 111
  i=v.rfind('.')
  if i>0:
    var= eval(v[:i])
    return getattr(var, v[i+1:])
  else:
    return eval(v)

def sv(v, newval): # set value var. or atribute US: gv('c.sub.s.a', 111)
  i=v.rfind('.')
  if i>0:
    var= eval(v[:i])
    try: setattr(var, v[i+1:], eval(newval))
    except: setattr(var, v[i+1:], newval)
  else:
      try:
          xy=eval(newval)+0
          globals()[v]=xy
      except:
          globals()[v]=newval

# Delete first line from file, which is returned
def getFirstLine(fname):
  if os.path.getsize(fname) > 0: # if have nonempty file
    f = open(fname, 'r')
    fw = open(fname+'.tmp' ,'w')
    first=''
    try:
      all_lines = f.readlines(); first=all_lines[0];
      for line in all_lines[1:]:
        fw.write(line)
    except: pass
    f.close()
    fw.close()
    os.rename(fname+'.tmp',fname)
    return first
  else:
    return ""

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

def handle_light():
  global lightOldOn
  if (stgs.lightStart+stgs.lightDuration > LIGHT_HOURS_LEAP):
    lightHours = range(stgs.lightStart,LIGHT_HOURS_LEAP) + range(0, stgs.lightStart+stgs.lightDuration-LIGHT_HOURS_LEAP)
  else:
    lightHours = range(stgs.lightStart, stgs.lightStart+stgs.lightDuration)
  currentHour=int(strftime("%H")) # int(strftime("%S")) # for testing, %H for production
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
  global tenMinutesRun
  tenMinutes=(strftime("%M")[1]=='0') # every 10 minutes
  if tenMinutesRun!=tenMinutes:
    if tenMinutes: 
      handle_light()
      handle_heating()
      handle_pomp()
      handle_pomp2()
  tenMinutesRun=tenMinutes

t=None; h=None; moisture=False;

while True: # Main loop begin
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
    log('Temp={0:0.1f}*C Hum={1:0.1f}% Moist={2}' .format(temperature, humidity, moisture))
  else: #turn leds off
    GPIO.setup(LED2, LedOFF)
    GPIO.setup(LED3, LedOFF)
    GPIO.setup(LED4, LedOFF)
  blinkTick=blinkTick+1
  if blinkTick>9223372036854775807: blinkTick=0
  cmd=getFirstLine(current_dir+"/pipe").strip() # read commands and variables set from other process
  if len(cmd)>0:
    if cmd.find('=')<0:
      if cmd=='logs':
        logs_file = open(current_dir+"/logs", "w")
        logs_file.write('\n'.join(logs) + '\n')
        logs_file.close()
        print("writing to file")
      else:
        try:
          log(cmd.strip()+"="+str(gv(cmd.strip())))
        except: pass
    else:
      try:
        sv(cmd[:cmd.find('=')].strip(), cmd[1+cmd.find('='):].strip())
        if "stgs.lightDuration"==cmd[:cmd.find('=')].strip(): handle_light()
      except: print "no such var, :", cmd[:cmd.find('=')]
  tenMinutesCheck()
  # Main loop end

# from chirp import Chirp
# chirp = Chirp(1, 0x6f)
# chirp.cap_sense()
# ex: et sw=2 ts=2
