import socket
from DeviceManager import DeviceManager

from Connector import Connector
from SaveSensorData import SaveSensorData
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用
host = "0.0.0.0" # 監聽哪個ip
port = 9999 # 串口位置
server_socket.bind((host, port)) # 綁定到socket上
server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶

try:
    # 連接各種模組
    dev_manager = DeviceManager()
    # data_Logger = SaveSensorData()

    while(True): # 不斷循環等待客戶連線
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")
        connector = Connector(client_socket, dev_manager) # 應該卡在這邊運行，完成後等待下一次連線
        
            
except Exception as e:
    print(f"連線區 發生錯誤: {e}")
    print("準備關閉伺服器...")
finally:
    server_socket.close()
    print("伺服器關閉。")
