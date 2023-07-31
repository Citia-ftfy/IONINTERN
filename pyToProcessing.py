import serial
import glob
import warnings
import serial.tools.list_ports
import virtualserialports
import sys
#import pyfirmata
import time
from asyncio import get_event_loop

virtualserialports.run(2, loopback=False, debug=False)
ser = serial.Serial()
ser = serial.Serial("/dev/pts/0", 57600, timeout=1)
msg = ser.read_until(b'\n')
i = 0


while(True):
    time.sleep(1)
    msg = ser.read_until(b'\n')
    print(msg)
    if(b'RESET' in msg):
        i=0
        print('reset '+str(i))
    elif(b'READY' in msg):
        i+=1
        if(i%10==5):
            ser.write(b'LOADtest.txt\n') #TODO
        else:
            print('skip'+str(i))

#MAKE THIS PROGRAM READ THE INCOMING STREAM

#ser.close()