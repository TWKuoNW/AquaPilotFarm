import socket
import threading
import time

from DeviceManager import DeviceManager
from Listener import Listener

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用
host = "0.0.0.0" # 監聽哪個ip
port = 9999 # 串口位置
server_socket.bind((host, port)) # 綁定到socket上
server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶


def save_sensor_data(air_temp_and_hum_sensor, water_temp_and_DO_sensor): # 儲存感測器資料的方法
    while(True):
        air_temperature = air_temp_and_hum_sensor.temperature
        air_humidity = air_temp_and_hum_sensor.humidity
        water_temperature = water_temp_and_DO_sensor.water_temperature
        water_DO = water_temp_and_DO_sensor.DO

        with open("sensor_data.txt", "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, AirTemperature: {air_temperature}C, AirHumidity: {air_humidity}%, WaterTemperature: {water_temperature}C, WaterDO: {water_DO}mg/L \n")
        
        time.sleep(60)

try:
    dev_manager = DeviceManager()
    air_temp_and_hum_obj = dev_manager.get_temp_and_hum_sensor_instance()
    water_temp_and_DO_obj = dev_manager.get_water_temp_and_DO_sensor_instance()
    ps_obj = dev_manager.get_probiotic_sprayer_instance()
    af_obj = dev_manager.get_auto_feeder_instance()

    save_sensor_data_thread = threading.Thread(target = save_sensor_data, daemon=True, args=(air_temp_and_hum_obj, water_temp_and_DO_obj,)) # 啟動數據儲存串流
    save_sensor_data_thread.start()

    while(True): # 不斷循環等待客戶連線
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")

        listener = Listener(client_socket, ps_obj, af_obj) # 啟動監聽器
        listener.start() # 啟動執行續

        try:
            while(True):
                air_temperature_and_humidity = "01 " + str(air_temp_and_hum_obj.temperature) + " " + str(air_temp_and_hum_obj.humidity) + "\r\n"
                client_socket.send(air_temperature_and_humidity.encode('utf-8'))
                time.sleep(1)
                
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
