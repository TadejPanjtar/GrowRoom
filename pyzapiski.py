LOGGING=True

def log(msg):
  if LOGGING:  print strftime("%Y-%m-%d %X"), msg

from time import strftime,sleep
from stgs import stgs

lightHours=[]
lightOldOn=False # read light status
LIGHT_HOURS_LEAP=24
LIGTH_HOURS_START=stgs.lightStart
LIGTH_HOURS_DURATION=stgs.lightDuration
tenMinutesRun=False
blinkTick=0

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
  lightOldOn=lightOn

print 'lightHours', lightHours

def tenMinutesCheck():
  global tenMinutesRun, blinkTick
  tenMinutes=(strftime("%S")[1]=='0') # every 10 minutes
  if tenMinutesRun!=tenMinutes:
    print "10 minutes"
    #if tenMinutes: 
    #  handle_light()
    #  handle_heating()
    #  handle_pomp2()
    #  handle_pomp()
    blinkTick=0
  tenMinutesRun=tenMinutes
  
t=None; h=None; moisture=33;

while True:
  if blinkTick % 3 == 0:
    print "sensor 1"
  if blinkTick % 3 == 1:
    print "sensor 2"  
  if blinkTick % 3 == 2:
    print "sensor 3" # TODO implement
    sleep(1)
  t=None; h=None; moisture=33;
  
  if t: # handle empty variable
    temperature=t
  
  if h:
    humidity=h
  
  if blinkTick % 2== 0: 
    print 'Temp={0:0.1f}*C Humidity={1:0.1f}% Moisture={1:0.1f}%' .format(temperature, humidity, moisture)
  blinkTick=blinkTick+1

    
