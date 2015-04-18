from time import strftime,sleep
import os

from stgs import stgs
LOGGING=True
heating=False

def logOld(msg):
  # if LOGGING:  print strftime("%Y-%m-%d %X"), msg
    if LOGGING:  print strftime("%d-%X"), msg

logs=[]
LOGS_SIZE=5

def log(msg):
  # if LOGGING:  print strftime("%Y-%m-%d %X"), msg
    if LOGGING:
      print strftime("%d-%X"), msg
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

dbg=True

while True:
  cmd=getFirstLine("pipe").strip() # read commands and variables set from other process
  if len(cmd)>0:
    if cmd.find('=')<0:
      if cmd=='d':
        logs_file = open("ttt", "w")
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
      except: print "no such var, :", cmd[:cmd.find('=')]
  sleep(2)
  cmd=""




# ex: et sw=2 ts=2
