import threading
import socket

def is_socket_connected(socket):
    try:
        # 發送一個非阻塞的零字節消息
        socket.send(b'\0')
    except Exception as e:
        return False  # 未連接
    return True  # 仍然連接

# 監聽器
class Transmitter(threading.Thread):
    def __init__(self, client_socket):  # 初始化Thread的設定
        super().__init__() # 調用父類別(Thread)的建構函式
        self.client_socket = client_socket # 獲取傳進來的socket
        self._stop_event = threading.Event() # 創建一個事件，用於執行續的同步

    def stop(self):
        self._stop_event.set() # 建立_stop_event標示為True，用於通知執行續的停止

    def stopped(self): # 這個function會回傳boolean型態，若有設置停止就會回傳True，反之為False
        return self._stop_event.is_set() # 檢查_stop_event標誌，如果設置了就返回True
            
    def run(self): # 執行續啟動後會啟動該function
        while(not self.stopped()): # 不斷循環直到檢查到_stop_event被設定
            try:
                is_socket_connected(self.client_socket)
                command = input("向客戶端發送:")
                self.client_socket.send(command.encode("utf-8")) # 向socket發送數據
                if(command == "EXIT"):
                    print("發送退出信號......")
                    self.stop()
            except socket.error as e:
                self.stop() # 若發生錯誤，列印錯誤訊息並停止執行續
                print(f"發送器 發生錯誤{e}")

        self.client_socket.close() # 循環結束，關閉socket連線
        print("發送器關閉")
