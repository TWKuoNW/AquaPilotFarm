import serial
import time
import os

def check_rfcomm1_existence():
    return os.path.exists('/dev/rfcomm1')

connect = False
if(check_rfcomm1_existence()):
	ser = serial.Serial("/dev/rfcomm1", 115200)
	connect = True

def open():
	if(connect):
		ser.write("c,0,0,1".encode())
		time.sleep(1.5)
		ser.write("c,0,4,1".encode())

	print("AutoFeeder.py::open()")
	
				
def close():
	if(connect):
		ser.write("c,0,0,0".encode())
		time.sleep(1.5)
		ser.write("c,0,4,0".encode())

	print("AutoFeeder.py::close()")
