import serial

class CameraControl:

    def __init__(self, device_path="/dev/ttyUSB0", baudrate=9600):
        self.ser = serial.Serial(device_path, baudrate)

    def turn_right(self):
        self.ser.write('r'.encode())
        print("相機向右轉")
        
    def turn_left(self):
        self.ser.write('l'.encode())
        print("相機向左轉")
        
