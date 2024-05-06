import serial

try:
	ser = serial.Serial("/dev/rfcomm1", 115200) 

	def open():
		# print("AutoFeeder.py:open")
		ser.write("1".encode())
		
	def close():
		# print("AutoFeeder.py:close")
		ser.write("0".encode())

except Exception as e:
	print(f"自動餵食器控制 發生錯誤{e}")

