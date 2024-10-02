# connector 測試，未來會刪掉
import threading
import socket
import time

# 監聽器
class Connector(threading.Thread):
    def __init__(self, client_socket):  # 初始化Thread的設定
        super().__init__() # 調用父類別(Thread)的建構函式
        self.client_socket = client_socket # 獲取傳進來的socket
        self.client_socket.send("isOpened".encode('utf-8')) # 告訴客戶端連線成功
        threading.Thread(target = self.listener, daemon = True).start()
        threading.Thread(target = self.transmitter, daemon = True).start()

    def listener(self): # 監聽器
        try:
            while(True):
                msg = self.client_socket.recv(1024).decode('utf-8') # 接收客戶端發來的訊息
                if(msg != ""):
                    print("收到:", msg)
                
                time.sleep(1)
        except Exception as e:
            print(f"接收區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")

    def transmitter(self):
        try:
            while(True):
                self.client_socket.send("水溫 20 度".encode('utf-8'))
                self.client_socket.send("pH 6".encode('utf-8'))
                time.sleep(1)
        except Exception as e:
            print(f"發送區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")

if __name__ == "__main__" :
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 建立伺服器端的socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 將socket定義為允許重複使用
    host = "0.0.0.0" # 監聽哪個ip
    port = 9999 # 串口位置
    server_socket.bind((host, port)) # 綁定到socket上
    server_socket.listen(5) # 讓socket進入伺服器模式，並且最大連接五個客戶
    
    while(True): # 不斷循環等待客戶連線
        print("等待客戶端連線...")
        client_socket, client_address = server_socket.accept() # 等待客戶端連線(accept方法會阻塞，直到連線成功才往下執行)
        print(f"連線地址: {str(client_address)}")
        # listener = Listener(client_socket, ps_obj, af_obj, air_temp_and_hum_obj, water_temp_and_DO_obj, camera_control_obj) # 啟動監聽器
        # listener.start() # 啟動執行續
        connector = Connector(client_socket) # 應該卡在這邊運行，完成後等待下一次連線
        



    
