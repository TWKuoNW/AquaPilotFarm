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
        
if(__name__ == "__main__"):
    import time
    ps = ProbioticSprayer()
    ps.open()
    time.sleep(3)
    ps.close()
