import socket
import time

from DeviceManager import DeviceManager
from Listener import Listener
from SaveSensorData import SaveSensorData

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用
host = "0.0.0.0" # 監聽哪個ip
port = 9999 # 串口位置
server_socket.bind((host, port)) # 綁定到socket上
server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶

try:
    dev_manager = DeviceManager() # 創建設備管理器
    air_temp_and_hum_obj = dev_manager.get_temp_and_hum_sensor_instance()
    water_temp_and_DO_obj = dev_manager.get_water_temp_and_DO_sensor_instance()
    ps_obj = dev_manager.get_probiotic_sprayer_instance()
    af_obj = dev_manager.get_auto_feeder_instance()
    
    if(air_temp_and_hum_obj != None and water_temp_and_DO_obj != None): # 如果溫濕度感測器和溶解氧、水溫感測器都存在
        SaveSensorData(air_temp_and_hum_obj, water_temp_and_DO_obj) # 啟動儲存感測器資料的執行續

    while(True): # 不斷循環等待客戶連線
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")

        listener = Listener(client_socket, ps_obj, af_obj, air_temp_and_hum_obj, water_temp_and_DO_obj) # 啟動監聽器
        listener.start() # 啟動執行續

        try:
            while(True):
                if(air_temp_and_hum_obj != None):
                    air_temperature_and_humidity = "01 " + str(air_temp_and_hum_obj.temperature) + " " + str(air_temp_and_hum_obj.humidity) + "\r\n"
                    client_socket.send(air_temperature_and_humidity.encode('utf-8'))
                    time.sleep(1)

                if(water_temp_and_DO_obj != None):
                    water_temperature_and_DO = "02 " + str(water_temp_and_DO_obj.water_temperature) + " " + str(water_temp_and_DO_obj.DO) + "\r\n"
                    client_socket.send(water_temperature_and_DO.encode('utf-8'))
                    time.sleep(1)
                
        except Exception as e:
            print(f"發送區 發生錯誤:{e}")
            print("關閉客戶端連線")
            
except Exception as e:
    print(f"連線區 發生錯誤: {e}")
    print("準備關閉伺服器...")
finally:
    server_socket.close()
    print("伺服器關閉。")
