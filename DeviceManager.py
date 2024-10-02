import os
import glob
import subprocess
import threading
import time
import cv2

from TempAndHumSensor import TempAndHumSensor
from WaterTempAndDOSensor import WaterTempAndDOSensor
from ProbioticSprayer import ProbioticSprayer
from AutoFeeder import AutoFeeder
from video0 import VideoStream as Camera0
from video1 import VideoStream as Camera1
from video2 import VideoStream as Camera2
from camera_control import CameraControl

class DeviceManager:
    def __init__(self):
        self.temp_and_hum_sensor = None
        self.water_temperature_and_DO_sensor = None
        self.probiotic_sprayer = None
        self.auto_feeder = None
        self.camera_control = None

        self.video0_is_connect = False
        self.video1_is_connect = False
        self.video2_is_connect = False
        
        self.camera_list = []
        print("設備管理器運作中，請稍後.....")

        print("搜尋裝置...")
        
        print("\t搜尋連接上樹梅派的USB與ACM裝置...")
        USB_list = self.check_devices('/dev/ttyUSB*')
        ACM_list = self.check_devices('/dev/ttyACM*')

        print("\t搜尋連接上藍牙裝置...")
        self.release_rfcomm_connections() # 釋放所有 rfcomm 連接
        bluetooth_devices_list = self.get_paired_bluetooth_devices()

        print("\t搜尋連接上樹梅派的相機...")
        for camera_idx in range(5):
            cap = cv2.VideoCapture(camera_idx)
            if(cap.isOpened()):
                self.camera_list.append(camera_idx)
                cap.release()
        
        print(f"\t找到USB: {USB_list}")
        print(f"\t找到ACM: {ACM_list}")
        print(f"\t找到藍牙裝置: {bluetooth_devices_list}")
        print(f"\t找到相機: {self.camera_list}")

        print("識別與綁定裝置...")
        
        for USB in USB_list:
            idVender, idProduct, serial = self.get_device_info(USB)
            print(f"USB:{USB}, idVender: {idVender}, idProduct: {idProduct}, serial: {serial}")
            if(idVender == '1a86' and idProduct == '7523' and serial == '0000'):
                print(f"\t識別到溫濕度感測器...")
                self.temp_and_hum_sensor = TempAndHumSensor(device_path = USB)
                print("\t啟動 TempAndHumSensor.py")
            elif(idVender == '1a86' and idProduct == '7523' and serial == '1a86_USB_Serial'):
                print("\t識別到相機控制器...")
                self.camera_control = CameraControl(device_path = USB)
                print("\t啟動 CameraControl.py")
            """
            elif(idVender == '0403' and idProduct == '6001' and serial == 'A9G3VPLP'):
                print("\t識別到溶解氧、水溫感測器...")
                self.water_temperature_and_DO_sensor = WaterTempAndDOSensor(device_path = USB)
                print("\t啟動 WaterTempAndDOSensor.py")
            """

        for ACM in ACM_list:
            idVender, idProduct, serial = self.get_device_info(ACM)
            # print(f"ACM: idVendor:{idVender}, idProduct:{idProduct}, Serial:{serial}")
            
            if(idVender == '2341' and idProduct == '0069' and serial == '33171E0937323835AACF33324B572D45'):
                print("\t識別到溶解氧、水溫感測器...")
                self.water_temperature_and_DO_sensor = WaterTempAndDOSensor(device_path = ACM)
                print("\t啟動 WaterTempAndDOSensor.py")
            

        for device in bluetooth_devices_list:
            addr, name = device['address'], device['name']
            if(name == "ProbioticSprayer"):
                print("\t識別到益生菌噴灑器...")
                self.bind_rfcomm(0, addr)
                print("\t益生菌噴灑器綁定完成")
                time.sleep(1)
                self.probiotic_sprayer = ProbioticSprayer()
                print("\t啟動 ProbioticSprayer.py")
            if(name == "AutoFeeder"):
                print("\t識別到自動餵食器...")
                self.bind_rfcomm(1, addr)
                print("\t自動餵食器綁定完成")
                time.sleep(1)
                self.auto_feeder = AutoFeeder()
                print("\t啟動 AutoFeeder.py")
        
        for video in self.camera_list:
            if(self.video0_is_connect == False):
                print("\t識別到第一支相機...")
                self.video0_is_connect = True
                threading.Thread(target=self.run_camera0, args=(video,)).start()
                print("\t第一支相機已啟動")
            elif(self.video1_is_connect == False):
                print("\t識別到第二支相機...")
                self.video1_is_connect = True
                threading.Thread(target=self.run_camera1, args=(video,)).start()
                print("\t第二支相機已啟動")
            elif(self.video2_is_connect == False):
                print("\t識別到第三支相機...")
                self.video2_is_connect = True
                threading.Thread(target=self.run_camera2, args=(video,)).start()
                print("\t第三支相機已啟動")

    def check_devices(self, dev): # 尋找 device
        devices = glob.glob(dev)
        device_list = []
        for device in devices:
            if os.path.exists(device):
                device_list.append(device)
        
        return device_list

    def get_device_info(self, device_path): # 取得 idVender 和 idProduct 
        try:
            result = subprocess.run(['sudo', 'udevadm', 'info', '-q', 'all', '-n', device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"Error running udevadm: {result.stderr}")
                return None, None

            vendor_id, product_id, serial = None, None, None
            for line in result.stdout.splitlines():
                if 'ID_VENDOR_ID' in line:
                    vendor_id = line.split('=')[1].strip()
                elif 'ID_MODEL_ID' in line:
                    product_id = line.split('=')[1].strip()
                elif 'ID_SERIAL' in line:
                    serial = line.split('=')[1].strip()
            
            return vendor_id, product_id, serial

        except Exception as e:
            print(f"Exception occurred: {e}")
            return None, None
    
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

    def get_paired_bluetooth_devices(self): # 取得已配對的藍牙裝置
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

    def bind_rfcomm(self, channel, device_address): # 把藍牙綁訂到 rfcomm            
        try:
            subprocess.check_call(['sudo', 'rfcomm', 'bind', str(channel), device_address, '1'])
            # print(f"綁定 {device_address} 到 RFCOMM channel {channel}")
        except subprocess.CalledProcessError as e:
            print(f"綁定失敗: {e}")
    
    def run_camera0(self, video): # 啟動相機0
        video_stream = Camera0(video)
        video_stream.run()

    def run_camera1(self, video): # 啟動相機1
        video_stream = Camera1(video)
        video_stream.run()

    def run_camera2(self, video): # 啟動相機2
        video_stream = Camera2(video)
        video_stream.run()

    def get_temp_and_hum_sensor_instance(self): # 取得溫濕度感測器物件
        return self.temp_and_hum_sensor
    
    def get_water_temp_and_DO_sensor_instance(self): # 取得溶解氧、水溫感測器物件
        return self.water_temperature_and_DO_sensor
    
    def get_probiotic_sprayer_instance(self): # 取得益生菌噴灑器物件
        return self.probiotic_sprayer
    
    def get_auto_feeder_instance(self): # 取得自動餵食器物件
        return self.auto_feeder

    def get_camera_control_instance(self): # 取得相機控制物件
        return self.camera_control   
if(__name__ == "__main__"):
    import time
    dev_manager = DeviceManager()
    air_temp_and_hum_obj = dev_manager.get_temp_and_hum_sensor_instance()
    water_temp_and_DO_obj = dev_manager.get_water_temp_and_DO_sensor_instance()
    ps_obj = dev_manager.get_probiotic_sprayer_instance()
    af_obj = dev_manager.get_auto_feeder_instance()
    
    print(ps_obj, " ", af_obj)

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
