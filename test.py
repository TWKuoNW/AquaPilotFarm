import os

def check_rfcomm0_existence():
    return os.path.exists('/dev/ttyUSB0')

rfcomm0_exists = check_rfcomm0_existence()
print(rfcomm0_exists)