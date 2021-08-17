import serial
import datetime
import time

address = '/dev/ttyUSB0'
BAUDRATE = 9600
numChars = 11 #Length in bytes of each message.

def getMagField():
    try:
        port = serial.Serial(address, BAUDRATE, bytesize = 8) 
        print(f"Successfully opened port at {address}")
    except serial.SerialException:
        Hx = 0
        Hy = 0
        Hz = 0#indicates an error in connection
        print("Error in port connection")
        return False
    else:
        x = port.read(numChars)
        
#         while x[0] != 85: #previous logic used; inefficient. 
#             port.close()
#             port = serial.Serial(address, BAUDRATE, bytesize = 8)
#         while x[1] != 84:
#             x = port.read(numChars)

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
        x = byte_string
        print(x)
        Hx = ((x[3] << 8) | x[4]) 
        Hy = ((x[5] << 8) | x[6]) 
        Hz = ((x[7] << 8) | x[8])
    
        if Hx <= 2**15 and Hy <= 2**15 and Hz <= 2**15: #half of a sixteen-bit value's range; this condition being met means all fields are positive.
             print(f"x: {Hx}, y: {Hy}, z: {Hz}")
             time = datetime.datetime.now()
             print(time)
        else:
             import sys
             b = Hx.to_bytes(2, byteorder=sys.byteorder, signed=False)
             Hx = int.from_bytes(b, byteorder=sys.byteorder, signed=True)
             b = Hy.to_bytes(2, byteorder=sys.byteorder, signed=False)
             Hy = int.from_bytes(b, byteorder=sys.byteorder, signed=True)
             b = Hz.to_bytes(2, byteorder=sys.byteorder, signed=False)
             Hz = int.from_bytes(b, byteorder=sys.byteorder, signed=True)
             print(f"x: {Hx}, y: {Hy}, z: {Hz}")
             time = datetime.datetime.now()
             print(time)
        port.close()
    return Hx
