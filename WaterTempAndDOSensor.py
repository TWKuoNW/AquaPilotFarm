import serial
import time
import threading

class WaterTempAndDOSensor:
    def __init__(self, device_path = ""):
        self.device_path = device_path
        self.command = "ALL"
        self.water_temperature = 0.0
        self.DO = 0.0
        
        start = threading.Thread(target = self.Reader)
        start.daemon = True
        start.start()

    def send(self, ser, command):
        ser.write(command.encode())
        response = ser.readline().decode()
        response = response.replace("\r\n", "").split(" ")       
        return response

    def Reader(self):
        ser = ""
        while(True):
            try:
                if(ser == ""):
                    ser = serial.Serial(self.device_path, 115200, timeout = 2)
                data = self.send(ser, "ALL")
                if(len(data) > 1):
                    self.water_temperature = data[0]
                    self.DO = int(data[1]) / 100
                time.sleep(1)

            except Exception as error_infomation:
                ser = ""
                print(error_infomation) 
                time.sleep(1)

if(__name__ == "__main__"):
    sensor = WaterTempAndDOSensor(device_path = "/dev/ttyACM0")
    for i in range(10):
        print("DO:", sensor.DO, " water_temp:", sensor.water_temperature)
        time.sleep(1)
    
