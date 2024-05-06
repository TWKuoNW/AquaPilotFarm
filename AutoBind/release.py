import subprocess

def release_rfcomm(rfcomm_device_id):
    try:
        # 使用 rfcomm 命令釋放裝置
        subprocess.check_call(['sudo', 'rfcomm', 'release', rfcomm_device_id])
        print(f"Released RFCOMM device {rfcomm_device_id}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to release: {e}")

if __name__ == "__main__":
    rfcomm_device_id = '0'  # 之前綁定時指定的設備號
    release_rfcomm(rfcomm_device_id)
    
    rfcomm_device_id = '1'  # 之前綁定時指定的設備號
    release_rfcomm(rfcomm_device_id)
