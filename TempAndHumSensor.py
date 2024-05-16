import serial
import time
import threading

class TempAndHumSensor:
    def __init__(self, device_path = ""):
        self.device_path = device_path
        self.command_set = ['01', '04', '00', '01', '00', '02', '20', '0B']
        self.temperature = 0.0
        self.humidity = 0.0
        
        start = threading.Thread(target = self.Reader)
        start.daemon = True
        start.start()


    def send(self, ser, command):
        command = bytes([int(x, 16) for x in command])
        ser.write(command) 
        response = ser.read(9)
        response = [format(x, '02x') for x in response]
        return response

    def Reader(self):
        ser = ""
        while(True):
            try:
                if(ser == ""):
                    ser = serial.Serial(port = self.device_path, baudrate = 9600, bytesize = 8, parity = 'N', stopbits = 1, timeout = 2) 
                data = self.send(ser = ser, command = self.command_set) # send command to device
                value1 = data[3] + data[4] # get the value
                value2 = data[5] + data[6] # get the value

                self.temperature = int(value1, 16) / 10 # convert hex to float
                self.humidity = int(value2, 16) / 10 # convert hex to float

                # print("Temperature: ", self.temperature, "°C")
                # print("Humidity: ", self.humidity, "%")        

                time.sleep(1) # delay 1 second            

            except Exception as error_infomation:
                ser = ""
                print(error_infomation) 
                time.sleep(1)

if(__name__ == "__main__"):
    sensor = TempAndHumSensor(device_path = '/dev/ttyUSB0')
    for i in range(10):
        print(sensor.temperature, sensor.humidity)
        time.sleep(1)
    
