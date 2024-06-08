import threading
import socket
import time

# 監聽器
class Listener(threading.Thread):
    def __init__(self, client_socket, ps_obj, af_obj, air_temp_and_hum_obj, water_temp_and_DO_obj):  # 初始化Thread的設定
        super().__init__() # 調用父類別(Thread)的建構函式
        self.client_socket = client_socket # 獲取傳進來的socket
        self._stop_event = threading.Event() # 創建一個事件，用於執行續的同步
        self.ps_obj = ps_obj # 獲取傳進來的 益生菌噴灑器 物件
        self.af_obj = af_obj # 獲取傳進來的 自動餵食器 物件
        self.air_temp_hum_obj = air_temp_and_hum_obj # 獲取傳進來的 溫濕度感測器 物件
        self.water_temp_and_DO_obj = water_temp_and_DO_obj # 獲取傳進來的 溶解氧、水溫感測器 物件

    def stop(self):
        self._stop_event.set() # 建立_stop_event標示為True，用於通知執行續的停止

    def stopped(self): # 這個function會回傳boolean型態，若有設置停止就會回傳True，反之為False
        return self._stop_event.is_set() # 檢查_stop_event標誌，如果設置了就返回True
        
    def autoFeeder_control(self, action): # 自動餵食器控制
        if(action == 'af1'):
            self.af_obj.open()
        elif(action == 'af0'):
            self.af_obj.close()
    
    def probioticSprayer_control(self, action): # 益生菌噴灑器控制
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
                    
                elif((data == "af1" or data == "af0") and self.af_obj != None): # 如果接收到的數據是af1或af0，並且自動餵食器物件存在
                    # print(data)
                    AutoFeeder = threading.Thread(target=self.autoFeeder_control, daemon=True, args=(data,)) # 創建一個執行續，用於控制自動餵食器
                    AutoFeeder.start() 

                elif((data == "ps1" or data == "ps0") and self.ps_obj != None): # 如果接收到的數據是ps1或ps0，並且益生菌噴灑器物件存在
                    # 使用執行續控制益生菌噴灑器，防止阻塞
                    ProbioticSprayer = threading.Thread(target=self.probioticSprayer_control, daemon=True, args=(data,)) 
                    ProbioticSprayer.start()

                elif(data == "Air_Temperature" and self.air_temp_hum_obj != None): # 如果接收到的數據是Air_Temperature，並且溫濕度感測器物件存在
                    self.client_socket.send(str(self.air_temp_hum_obj.temperature).encode('utf-8'))
                    print(str(self.air_temp_hum_obj.temperature))

                elif(data == "Air_Humidity" and self.air_temp_hum_obj != None): # 如果接收到的數據是Air_Humidity，並且溫濕度感測器物件存在
                    self.client_socket.send(str(self.air_temp_hum_obj.humidity).encode('utf-8'))
                    print(str(self.air_temp_hum_obj.humidity))

                elif(data == "Water_Temperature" and self.water_temp_and_DO_obj != None): # 如果接收到的數據是Water_Temperature，並且溶解氧、水溫感測器物件存在
                    self.client_socket.send(str(self.water_temp_and_DO_obj.water_temperature).encode('utf-8'))
                    print(str(self.water_temp_and_DO_obj.water_temperature))

                elif(data == "Water_DO" and self.water_temp_and_DO_obj != None): # 如果接收到的數據是Water_DO，並且溶解氧、水溫感測器物件存在
                    self.client_socket.send(str(self.water_temp_and_DO_obj.DO).encode('utf-8'))
                    print(str(self.water_temp_and_DO_obj.DO))  
                    
                elif(data != ""):
                    print(f"收到PC訊息: {data}") 

            except socket.error as e:
                self.stop() # 若發生錯誤，列印錯誤訊息並停止執行續
                print(f"監聽區 發生錯誤{e}")
            time.sleep(1)

        self.client_socket.close() # 循環結束，關閉socket連線
        print("監聽器關閉")
