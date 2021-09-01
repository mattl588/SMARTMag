#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#% WitMotionCode.py
#% Author: Matt Lacaire
#% Code that is a Python adaptation of WitMotion's
#% RM3100 code. 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import serial
import datetime
import datetime
address = '/dev/ttyUSB0'
BAUDRATE = 9600
numChars = 11 #Length in bytes of each message. 


def twos(val_str, bytes): #performs two's complement operation. This is roundabout, but the x object is returned in decimal for some reason.
    import sys
    b = val_str.to_bytes(bytes, byteorder=sys.byteorder, signed=False)
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)


def ParseData(dataarray):

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

    #return Hx, Hy, Hz


# # 
if __name__ == "__main__":
    try:
        port = serial.Serial(address, BAUDRATE, bytesize = 8) 
        print(f"Successfully opened port at {address}")
    except serial.SerialException:
        Hx = 0
        Hy = 0
        Hz = 0#indicates an error in connection
        print("Error in port connection")
    keeploop = True
    while(keeploop):
        byte_string = b""
        read_continue = True
        while read_continue:
            end_line = False
            read_char = port.read(1)        
            if read_char == b"U":
                end_line = True
            elif len(byte_string) >= numChars:
                end_line = True
            else:
                byte_string += read_char
                
            if len(byte_string) > 0:
                if byte_string[0] != 85:
                    byte_string = b""
                    read_continue = True
                    continue
            if len(byte_string) > 1:
                if byte_string[1] != 84:
                    byte_string = b""
                    read_continue = True
                    continue
                
            if end_line:
                if len(byte_string) < numChars:
                    byte_string = read_char
                    read_continue = True
                else:
                    read_continue = False
            if read_continue == False and len(byte_string) == 11:
                x = ParseData(byte_string)
