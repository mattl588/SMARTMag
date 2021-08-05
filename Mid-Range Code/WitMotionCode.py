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

def ParseData(dataarray):
    if dataarray[0] == 85 and dataarray[1] == 84:
        Hx = ((dataarray[3] << 8) | dataarray[4]) 
        Hy = ((dataarray[5] << 8) | dataarray[6]) 
        Hz = ((dataarray[7] << 8) | dataarray[8])
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
