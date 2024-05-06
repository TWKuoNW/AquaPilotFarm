import socket
import temp_sensor_interface_V3_1 as sensor
import threading
import time
from Listener import Listener
from BTAutoBind import BTAutoBind
from video0 import app

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用

host = "0.0.0.0" # 監聽哪個ip
port = 9999 # 串口位置

server_socket.bind((host, port)) # 綁定到socket上
server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶


def run_video0(): # 定義 video0
    app.run(host='0.0.0.0', port=8000, threaded=True) 

try:
    sr = sensor.SensorReader() # 啟動感測器讀取器
    flask_thread = threading.Thread(target = run_video0) # 啟動video0串流
    flask_thread.start() # 啟動執行續
    bt_auto_bind = BTAutoBind()

    while(True): # 不斷循環等待客戶連線
        
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")

        listener = Listener(client_socket) # 啟動監聽器
        listener.start() # 啟動執行續

        try:
            while(True):
                air_temperature_and_humidity = "01 " + str(sr.read_value("TEMPERATURE")) + " " + str(sr.read_value("HUMIDITY")) + "\r\n"
                client_socket.send(air_temperature_and_humidity.encode('utf-8'))
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
