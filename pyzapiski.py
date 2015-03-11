LOGGING=True

def log(msg):
  if LOGGING:  print strftime("%Y-%m-%d %X"), msg

from time import strftime,sleep

lightHours=[]
lightOldOn=False # read light status
LIGHT_HOURS_LEAP=24
LIGTH_HOURS_START=22
LIGTH_HOURS_DURATION=16
tenMinutesRun=False

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
  global tenMinutesRun
  tenMinutes=(strftime("%S")[1]=='0') # every 10 minutes
  if tenMinutesRun!=tenMinutes:
    print "10 minutes"
    #if tenMinutes: 
    #  handle_light()
    #  handle_heating()
    #  handle_pomp2()
    #  handle_pomp()
  tenMinutesRun=tenMinutes
  

