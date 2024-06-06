import serial

class AutoFeeder:

    def __init__(self, device_path="/dev/rfcomm1", baudrate=115200):
        self.ser = serial.Serial(device_path, baudrate)

    def open(self):
        self.ser.write("1".encode())
        print("AutoFeeder.py::open()")
        
    def close(self):
        self.ser.write("0".encode())
        print("AutoFeeder.py::close()")