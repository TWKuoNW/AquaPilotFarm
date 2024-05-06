import os
import serial

def list_serial_devices():
    devices = []
    dev_directory = '/dev'

    for file in os.listdir(dev_directory):
        if(file.startswith('rfcomm')):
            devices.append(file)

    return devices

all_devices = list_serial_devices()
bluetooth_device = []

for rfcomm in all_devices:
    port = '/dev/' + rfcomm
    ser = serial.Serial(port, 115200)
    bluetooth_device.append(ser)
print("Detected devices:", bluetooth_device)
