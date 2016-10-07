from serial import Serial

data = Serial("/dev/ttyACM0",115200)

while(1 == 1):
    print data.readline()