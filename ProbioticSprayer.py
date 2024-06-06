import serial

class ProbioticSprayer:

    def __init__(self, device_path="/dev/rfcomm0", baudrate=115200):
        self.ser = serial.Serial(device_path, baudrate)

    def open(self):
        self.ser.write("open".encode())
        print("ProbioticSprayer.py::open()")
        
                    
    def close(self):
        self.ser.write("close".encode())
        print("ProbioticSprayer.py::close()")
