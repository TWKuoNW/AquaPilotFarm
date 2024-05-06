import os

def list_mapped_rfcomm_devices():
    rfcomm_path = '/dev'
    rfcomm_devices = [device for device in os.listdir(rfcomm_path) if device.startswith('rfcomm')]

    if rfcomm_devices:
        print("Found RFCOMM devices:")
        for device in rfcomm_devices:
            print(os.path.join(rfcomm_path, device))
    else:
        print("No RFCOMM devices found.")

if __name__ == "__main__":
    list_mapped_rfcomm_devices()
