import xml.etree.ElementTree as ET
import serial
import time
import threading

class SensorReader:
    # consructor
    def __init__(self):
        self.temperature = 0.0
        self.humidity = 0.0
        self.sensor_types = {}
        self.path = "/home/pi/AquaPlayerFarm/SensorType.xml"
        self.comport = "/dev/ttyUSB0" # define comport

        send_thread = threading.Thread(target=self.send)
        send_thread.daemon = True # open deamon thread
        send_thread.start()

    def read_value(self, sensor_type):
        try:
            self.sensor_types = self.create_sensor_type_from_xml(self.path)
            if sensor_type == self.sensor_types[0]:
                value = self.temperature
                #print(self.temperature)
            elif sensor_type == self.sensor_types[1]:
                value = self.humidity
            else:
                raise ValueError("Unsupported sensor type")
            # print("value = ", value)
            return value
        except:
            print("XML path error.")
        

    def send(self): # Thread
        ser = ""
        while(True):   
            try:
                if(ser == ""): 
                    ser = serial.Serial(self.comport, baudrate=9600, timeout=2)
                origin_send = ["01", "04", "00", "01", "00", "02", "20", "0B"]
                bytes_send = bytes([int(x, 16) for x in origin_send]) 
                ser.write(bytes_send)
                time.sleep(1)
                data = ser.read(9) 
                data = [format(x, '02x') for x in data]
                value1 = data[3] + data[4]
                value2 = data[5] + data[6]
                self.temperature = int(value1, 16) / 10
                self.humidity = int(value2, 16) / 10
            except:
                ser = ""
                # print("COM PORT ERROR Trying to reconnect.") 
                time.sleep(1)
                continue
    def setSerialPort(self, serial_port):
        self.comport = serial_port

    def setXMLPath(self, path):
        try:
            self.path = path
            self.sensor_types = self.create_sensor_type_from_xml(self.path)
        except: 
            print("XML path error.")
    
    def getXMLPath(self):
        print(self.path)

    def getSensorType(self):
        return self.sensor_types

    
    def create_sensor_type_from_xml(self, xml_path):
        sensor_types = {}
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for enum in root.findall(".//enum[@name='SENSOR_TYPE']/entry"):
            name = enum.get('name')
            value = int(enum.get('value'))
            sensor_types[value] = name
        return sensor_types
        
if __name__ == "__main__":
    s = SensorReader()
    while(True):
        s.read_value("TEMPERATURE")
        time.sleep(0.5)
