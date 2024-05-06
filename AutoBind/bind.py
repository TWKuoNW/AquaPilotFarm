import subprocess

def bind_rfcomm(channel, device_address): # 把藍牙綁訂到 rfcomm
    try:
        subprocess.check_call(['sudo', 'rfcomm', 'bind', str(channel), device_address, '1'])
        print(f"綁定 {device_address} 到 RFCOMM channel {channel}")
    except subprocess.CalledProcessError as e:
        print(f"綁定失敗: {e}")


if __name__ == "__main__":
    # 假設你已經知道了裝置的地址和要綁定的通道
    device_address = "E8:6B:EA:C9:AA:26"  # 用你的裝置地址替換
    channel = 1  # 通常是 1，但可能根據裝置而異
    bind_rfcomm(device_address, channel)
