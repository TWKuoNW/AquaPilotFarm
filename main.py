import socket
import threading
import time

from TempAndHumSensor import TempAndHumSensor
from WaterTempAndDOSensor import WaterTempAndDOSensor
from Listener import Listener
from BTAutoBind import BTAutoBind 
from video0 import app as app0
from video1 import app as app1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用
host = "0.0.0.0" # 監聽哪個ip
port = 9999 # 串口位置
server_socket.bind((host, port)) # 綁定到socket上
server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶

def run_video0(): # 定義 video0
    app0.run(host='0.0.0.0', port=8000, threaded=True) 

def run_video1(): # 定義 video1
    app1.run(host='0.0.0.0', port=8001, threaded=True) 

try:
    video_0 = threading.Thread(target = run_video0) # 啟動video0串流
    video_1 = threading.Thread(target = run_video1) # 啟動video0串流
    video_0.start() # 啟動執行續
    video_1.start() # 啟動執行續

    temp_and_hum_sensor = TempAndHumSensor(device_path = "/dev/ttyUSB0")
    water_temperature_and_DO_sensor = WaterTempAndDOSensor(device_path = "/dev/ttyACM0")

    bt_auto_bind = BTAutoBind() 

    while(True): # 不斷循環等待客戶連線
        
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")

        listener = Listener(client_socket) # 啟動監聽器
        listener.start() # 啟動執行續

        try:
            while(True):
                air_temperature_and_humidity = "01 " + str(temp_and_hum_sensor.temperature) + " " + str(temp_and_hum_sensor.humidity) + "\r\n"
                client_socket.send(air_temperature_and_humidity.encode('utf-8'))
                time.sleep(1)
                water_temperature_and_DO = "02 " + str(water_temperature_and_DO_sensor.water_temperature) + " " + str(water_temperature_and_DO_sensor.DO) + "\r\n"
                client_socket.send(water_temperature_and_DO.encode('utf-8'))
                # print(air_temperature_and_humidity)
                # print(water_temperature_and_DO)
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
