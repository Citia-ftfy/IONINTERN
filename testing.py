import zmq
import serial
import numpy as np
import serialFetch as sF
import argparse




CMD_SETPOSITION = "C09,"

ser = sF.get_Serial_Conn()



command = CMD_SETPOSITION+str(int(40+0.5))+","+str(int(40+0.5))+",END"
command.encode('utf-8')

#ba = bytes(command, encoding="ascii")
print(ser.read())
ser.write(command.encode())
ser.write(10)
ser.close()