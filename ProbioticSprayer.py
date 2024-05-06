import serial
import time

try:
	ser = serial.Serial("/dev/rfcomm0", 115200)
	probiotic_sprayer_online = True
except Exception as e:
	print(f"益生菌噴灑器控制 發生錯誤{e}")
	probiotic_sprayer_online = False
	
def open():
	if(probiotic_sprayer_online):
		ser.write("c,0,0,1".encode())
		time.sleep(1.5)
		ser.write("c,0,4,1".encode())
	else:
		print("ProbioticSprayer.py:open")
	
				
def close():
	if(probiotic_sprayer_online):
		ser.write("c,0,0,0".encode())
		time.sleep(1.5)
		ser.write("c,0,4,0".encode())
	else:
		print("ProbioticSprayer.py:close")
