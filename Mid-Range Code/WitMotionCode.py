#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#% WitMotionCode.py
#% Author: Matt Lacaire
#% Code that is a Python adaptation of WitMotion's
#% RM3100 code. 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import os
import serial
import time
address = '/dev/ttyUSB0'
BAUDRATE = 9600
numChars = 11 #I don't think this can change. This is how many characters are in a message to be parsed. 

def openSerial():
    ser = serial.Serial(address, BAUDRATE, bytesize = 8) #this should be correct. 
    return ser

def ParseData(dataarray):
    if dataarray[0] == 85 and dataarray[1] == 84:
        Hx = ((dataarray[3] << 8) | dataarray[4]) 
        Hy = ((dataarray[5] << 8) | dataarray[6]) 
        Hz = ((dataarray[7] << 8) | dataarray[8])
        print(f"x: {Hx}, y: {Hy}, z: {Hz}")
    else:
        print("Other data type")




port = openSerial()

if (port):
    print(f"Successfully opened port at {address}")
else:
    print("Port Opening Failure") #deal with this later
    
while(port.is_open):
    x = port.read(numChars)
    ParseData(x)

    

       
    
    
    
    
