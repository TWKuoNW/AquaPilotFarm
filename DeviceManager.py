import os
import glob
import subprocess
import bluetooth
import threading

from TempAndHumSensor import TempAndHumSensor
from WaterTempAndDOSensor import WaterTempAndDOSensor
from ProbioticSprayer import ProbioticSprayer
from AutoFeeder import AutoFeeder
from video0 import app as app0
from video1 import app as app1

class DeviceManager:
    def check_devices(self, dev): # 尋找 device
        devices = glob.glob(dev)
        device_list = []
        for device in devices:
            if os.path.exists(device):
                device_list.append(device)
        
        return device_list

    def get_device_info(self, device_path): # 取得 idVender 和 idProduct 
        try:
            result = subprocess.run(['udevadm', 'info', '-q', 'all', '-n', device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"Error running udevadm: {result.stderr}")
                return None, None

            vendor_id, product_id = None, None
            for line in result.stdout.splitlines():
                if 'ID_VENDOR_ID' in line:
                    vendor_id = line.split('=')[1].strip()
                elif 'ID_MODEL_ID' in line:
                    product_id = line.split('=')[1].strip()
            
            return vendor_id, product_id

        except Exception as e:
            print(f"Exception occurred: {e}")
            return None, None
    
    def bind_rfcomm(self, channel, device_address): # 把藍牙綁訂到 rfcomm
        try:
            subprocess.check_call(['sudo', 'rfcomm', 'bind', str(channel), device_address, '1'])
            print(f"綁定 {device_address} 到 RFCOMM channel {channel}")
        except subprocess.CalledProcessError as e:
            print(f"綁定失敗: {e}")

    def run_video0(self): # 定義 video0
        app0.run(host='0.0.0.0', port=8000, threaded=True) 

    def run_video1(self): # 定義 video1
        app1.run(host='0.0.0.0', port=8001, threaded=True) 

    def __init__(self):
        self.temp_and_hum_sensor = None
        self.water_temperature_and_DO_sensor = None
        self.video0 = None
        self.Video1 = None
        self.probiotic_sprayer = None
        self.auto_feeder = None
        self.video0_is_connect = False
        self.video1_is_connect = False

        print("設備管理器運作中，請稍後.....")

        print("搜尋附近藍牙裝置...")

        nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5, flush_cache=True) # 附近藍芽設備
        
        print(f"找到 {len(nearby_devices)} 個藍牙設備")

        print("搜尋連接上樹梅派的USB與ACM裝置...")

        USB_list = self.check_devices('/dev/ttyUSB*')
        ACM_list = self.check_devices('/dev/ttyACM*')
        Video_list = self.check_devices('/dev/video*')

        for USB in USB_list:
            idVender, idProduct = self.get_device_info(USB)
            if(idVender == '1a86' and idProduct == '7523'):
                self.temp_and_hum_sensor = TempAndHumSensor(device_path = USB)
                print("啟動 TempAndHumSensor.py")

        for ACM in ACM_list:
            idVender, idProduct = self.get_device_info(ACM)
            if(idVender == '2341' and idProduct == '0043'):
                self.water_temperature_and_DO_sensor = WaterTempAndDOSensor(device_path = ACM)
                print("啟動 WaterTempAndDOSensor.py")

        for addr, name in nearby_devices:
            if(name == "ProbioticSprayer"):
                self.bind_rfcomm(0, addr)
                print("益生菌噴灑器綁定完成")
                self.probiotic_sprayer = ProbioticSprayer()
                print("啟動 ProbioticSprayer.py")

            if(name == "AutoFeeder"):
                self.bind_rfcomm(1, addr)
                print("自動餵食器綁定完成")
                self.auto_feeder = AutoFeeder()
                print("啟動 AutoFeeder.py")
    
        for video in Video_list:
            idVender, idProduct = self.get_device_info(video)
            if(idVender == '0c45' and idProduct == '636f' and self.video0_is_connect == False):
                print("open Video0")
                video_0 = threading.Thread(target = self.run_video0) # 啟動video0串流
                video_0.start() # 啟動執行續
                self.video0_is_connect = True
            elif(idVender == '13d3' and idProduct == '784b' and self.video1_is_connect == False):
                print("open Video1")
                video_1 = threading.Thread(target = self.run_video1) # 啟動video0串流
                video_1.start() # 啟動執行續
                self.video1_is_connect = True     

    def get_temp_and_hum_sensor_instance(self): # 取得溫濕度感測器物件
        return self.temp_and_hum_sensor
    
    def get_water_temp_and_DO_sensor_instance(self): # 取得溶解氧、水溫感測器物件
        return self.water_temperature_and_DO_sensor
    
    def get_probiotic_sprayer_instance(self): # 取得益生菌噴灑器物件
        return self.probiotic_sprayer
    
    def get_auto_feeder_instance(self): # 取得自動餵食器物件
        return self.auto_feeder
    
if(__name__ == "__main__"):
    import time
    dev_manager = DeviceManager()
    air_temp_and_hum_obj = dev_manager.get_temp_and_hum_sensor_instance()
    water_temp_and_DO_obj = dev_manager.get_water_temp_and_DO_sensor_instance()
    ps_obj = dev_manager.get_probiotic_sprayer_instance()
    af_obj = dev_manager.get_auto_feeder_instance()

    if(ps_obj != None):
        ps_obj.open()
        time.sleep(2)
        ps_obj.close()
        time.sleep(2)

    if(af_obj != None):
        af_obj.open()
        time.sleep(2)
        af_obj.close()
        time.sleep(2)
    
    while(True):
        if(air_temp_and_hum_obj != None):
            print(f"空氣溫度:{air_temp_and_hum_obj.temperature}, 空氣濕度:{air_temp_and_hum_obj.humidity}")
        if(water_temp_and_DO_obj != None):
            print(f"水中溫度:{water_temp_and_DO_obj.water_temperature}, 水中溶氧:{water_temp_and_DO_obj.DO}")
        time.sleep(5)
