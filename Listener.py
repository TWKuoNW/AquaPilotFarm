import threading
import socket
import time

# 監聽器
class Listener(threading.Thread):
    def __init__(self, client_socket, ps_obj, af_obj):  # 初始化Thread的設定
        super().__init__() # 調用父類別(Thread)的建構函式
        self.client_socket = client_socket # 獲取傳進來的socket
        self._stop_event = threading.Event() # 創建一個事件，用於執行續的同步
        self.ps_obj = ps_obj
        self.af_obj = af_obj

    def stop(self):
        self._stop_event.set() # 建立_stop_event標示為True，用於通知執行續的停止

    def stopped(self): # 這個function會回傳boolean型態，若有設置停止就會回傳True，反之為False
        return self._stop_event.is_set() # 檢查_stop_event標誌，如果設置了就返回True
        
    def autoFeeder_control(self, action):
        if(action == 'af1'):
            self.af_obj.open()
        elif(action == 'af0'):
            self.af_obj.close()
    
    def probioticSprayer_control(self, action):
        if(action == 'ps1'):
            self.ps_obj.open()
        elif(action == 'ps0'):
            self.ps_obj.close()
            
    def run(self): # 執行續啟動後會啟動該function
        while(not self.stopped()): # 不斷循環直到檢查到_stop_event被設定
            try:
                data = self.client_socket.recv(1024).decode("utf-8") # 從socket接收數據
                
                if(data == "EXIT"):
                    print("收到退出信號......")
                    self.stop()
                    print("退出執行續")
                    
                elif(data == "af1" or data == "af0"):
                    # print(data)
                    AutoFeeder = threading.Thread(target=self.autoFeeder_control, daemon=True, args=(data,))
                    AutoFeeder.start()

                elif(data == "ps1" or data == "ps0"):
                    ProbioticSprayer = threading.Thread(target=self.probioticSprayer_control, daemon=True, args=(data,))
                    ProbioticSprayer.start()

                elif(data == "video0_open"):
                    print(f"相機啟動...")

                elif(data != ""):
                    print(f"收到PC訊息: {data}") 
                
            except socket.error as e:
                self.stop() # 若發生錯誤，列印錯誤訊息並停止執行續
                print(f"監聽區 發生錯誤{e}")
            time.sleep(1)

        self.client_socket.close() # 循環結束，關閉socket連線
        print("監聽器關閉")
