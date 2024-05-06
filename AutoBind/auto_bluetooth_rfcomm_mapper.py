import bluetooth
import subprocess

def bind_rfcomm(channel, device_address): # 把藍牙綁訂到 rfcomm
    try:
        subprocess.check_call(['sudo', 'rfcomm', 'bind', str(channel), device_address, '1'])
        print(f"綁定 {device_address} 到 RFCOMM channel {channel}")
    except subprocess.CalledProcessError as e:
        print(f"綁定失敗: {e}")

print("搜尋附近藍牙裝置...")

nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5, flush_cache=True)
print(f"找到 {len(nearby_devices)} 個藍牙設備")

for addr, name in nearby_devices:
    if(name == "ProbioticSprayer"):
        bind_rfcomm(0, addr)
    if(name == "AutoFeeder"):
        bind_rfcomm(1, addr)
    # print(f"  Address: {addr} - Name: {name}")
    
    

