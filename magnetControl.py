#python for grabbing ardunio and allowing it to control an electromagnet
import serial
import glob
import warnings
import serial.tools.list_ports
import sys
import pyfirmata
import time




def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            
            s.write(str.encode("255/"))
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

porty = serial_ports()
if(len(porty)<1):
    raise Exception("No Port for magnet control in magnetControl.py")
ser = serial.Serial(porty[0], 9800, timeout=1)



def set_high():
    print("Setting High")  
    ser.write(b'H')
    time.sleep(0.1)
    
def set_low():
    print("Setting Low")  
    ser.write(b'L')
    time.sleep(0.1)
