import subprocess
import time

def release_rfcomm_connections(self): # 釋放所有 rfcomm 連接
    result = subprocess.run(['rfcomm'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    connections = []

    for line in output.split('\n'):
        if line.startswith('rfcomm'):
            parts = line.split()
            device = parts[0]
            connections.append(device)
    
    for device in connections:
        # print(f"Releasing {device}")
        subprocess.run(['sudo', 'rfcomm', 'release', device])

def get_paired_bluetooth_devices(): # 取得已配對的藍牙裝置
    # 進入 bluetoothctl 並執行指令
    process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=b'devices\nexit\n')
    
    devices = []
    for line in stdout.decode('utf-8').split('\n'):
        if 'Device' in line:
            parts = line.split(' ')
            device_address = parts[1]
            device_name = ' '.join(parts[2:])
            devices.append({'address': device_address, 'name': device_name})
    
    return devices

def bind_rfcomm(channel, device_address): # 把藍牙綁訂到 rfcomm            
    try:
        subprocess.check_call(['sudo', 'rfcomm', 'bind', str(channel), device_address, '1'])
        # print(f"綁定 {device_address} 到 RFCOMM channel {channel}")
    except subprocess.CalledProcessError as e:
        print(f"綁定失敗: {e}")

release_rfcomm_connections() # 釋放所有 rfcomm 連接
bluetooth_devices_list = get_paired_bluetooth_devices()
for device in bluetooth_devices_list:
    addr, name = device['address'], device['name']
    if(name == "AutoFeeder"):
        print("\t識別到自動餵食器...")
        bind_rfcomm(0, addr)
        time.sleep(1)
        probiotic_sprayer = ProbioticSprayer()
        print("\t啟動 ProbioticSprayer.py")
    

if __name__ == "__main__":
    print(get_paired_bluetooth_devices())


"""
檢查配對



"""