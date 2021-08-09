#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#% WitMotionCode.py
#% Author: Matt Lacaire
#% Code that is a Python adaptation of WitMotion's
#% RM3100 code. 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import serial
import datetime
import time
address = '/dev/ttyUSB0'
BAUDRATE = 9600
numChars = 11 #Length in bytes of each message. 

def openSerial():
    ser = serial.Serial(address, BAUDRATE, bytesize = 8) 
    return ser

def twos(val_str, bytes): #performs two's complement operation. This is roundabout, but the x object is returned in decimal for some reason.
    import sys
    b = val_str.to_bytes(bytes, byteorder=sys.byteorder, signed=False)
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)


def ParseData(dataarray):
    if dataarray[0] == 85 and dataarray[1] == 84:
        Hx = ((dataarray[3] << 8) | dataarray[4]) 
        Hy = ((dataarray[5] << 8) | dataarray[6]) 
        Hz = ((dataarray[7] << 8) | dataarray[8])
        if Hx <= 2**15 and Hy <= 2**15 and Hz <= 2**15: #half of a sixteen-bit value's range; this condition being met means all fields are positive.
            print(f"x: {Hx}, y: {Hy}, z: {Hz}")
            time = datetime.datetime.now()
            print(time)
        else:
            Hx = twos(Hx, 2)
            Hy = twos(Hy, 2)
            Hz = twos(Hz, 2)
            print(f"x: {Hx}, y: {Hy}, z: {Hz}")
            time = datetime.datetime.now()
            print(time)


try:
    port = openSerial()
    print(f"Successfully opened port at {address}")
except serial.SerialException:
    print("Port Opening Failure") #deal with this later
    time.sleep(1)
    exit() 


while(port.is_open):
    x = port.read(numChars)
    if x[0] == 85:
        ParseData(x)
    else:
        print("Bytestring not properly synced. Trying again...")
        port.close()
        port = openSerial()
