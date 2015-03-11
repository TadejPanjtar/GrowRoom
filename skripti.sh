# TESTING
cd /sys/class/gpio/
for i in {2..29}; do echo $i >export ; done
for i in {2..29}; do echo $i $(cat gpio$i/direction); done
for i in {2..29}; do echo out> gpio$i/direction; done

# OPENING TO WORK WITH PYTHON correctly and shell script
for i in 27 22 23 24 26 13 5 6; do 
  echo $i >/sys/class/gpio/export
  echo out >/sys/class/gpio/gpio$i/direction;
done
