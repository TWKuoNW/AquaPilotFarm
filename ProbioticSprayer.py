import serial
import time

ser = serial.Serial("/dev/rfcomm0", 115200)

def open():
	ser.write("c,0,0,1".encode())
	time.sleep(1.5)
	ser.write("c,0,4,1".encode())

	print("ProbioticSprayer.py::open()")
	
				
def close():
	ser.write("c,0,0,0".encode())
	time.sleep(1.5)
	ser.write("c,0,4,0".encode())

	print("ProbioticSprayer.py::close()")
