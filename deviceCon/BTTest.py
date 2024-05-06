import serial

ser =serial.Serial("/dev/rfcomm0", 115200) 
s = "0"
while(s != 'q'):
	command = s.encode("UTF-8")
	ser.write(command)
	s = str(input("please input status:"))

print(command)
