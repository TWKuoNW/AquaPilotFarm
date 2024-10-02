# connector 測試，未來會刪掉
import threading
import socket
import time
import re

# 監聽器
class Connector():
    def __init__(self, client_socket, dev_manager):  # 初始化Thread的設定
        self.client_socket = client_socket # 獲取傳進來的socket
        self.dev_manager = dev_manager # 獲取傳進來的dev_manager
        number_of_cameras = len(self.dev_manager.camera_list)
        trans_dev_manager_info = f"80 00 {number_of_cameras}"
        self.transmitter(trans_dev_manager_info)
        threading.Thread(target = self.listener, daemon = True).start()
        threading.Thread(target = self.transmit_sensor_value, daemon = True).start()
    def transmit_sensor_value(self):
        try:
            while(True):
                if(self.dev_manager.temp_and_hum_sensor != None):
                    air_temperature_and_humidity = "01 " + str(self.dev_manager.temp_and_hum_sensor.temperature) + " " + str(self.dev_manager.temp_and_hum_sensor.humidity) + "\r\n"
                    self.client_socket.send(air_temperature_and_humidity.encode('utf-8'))
                    #print(air_temperature_and_humidity)
                    time.sleep(1)
                if(self.dev_manager.water_temperature_and_DO_sensor != None):
                    water_temperature = "01 00 " + str(self.dev_manager.water_temperature_and_DO_sensor.water_temperature)                  
                    self.client_socket.send(water_temperature.encode('utf-8'))
                    time.sleep(1)
                    water_DO =  "01 01 " + str(self.dev_manager.water_temperature_and_DO_sensor.DO)
                    self.client_socket.send(water_DO.encode('utf-8'))
                    time.sleep(1)
                time.sleep(1)
            
        except Exception as e:
            print(f"發送區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")
            
    def listener(self): # 監聽器
        try:
            while(True):
                msg = self.client_socket.recv(1024).decode('utf-8') # 接收客戶端發來的訊息
                if(self.is_valid_format(msg)):
                    msg_list = [int(x, 10) for x in msg.split()]
                    self.process_list(msg_list)
                    # print(msg_list)
                if(msg != ""):
                    print("收到:", msg)
                
                time.sleep(1)
        except Exception as e:
            print(f"接收區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")

    def transmitter(self, msg):
        try:
            self.client_socket.send(str(msg).encode('utf-8'))
            print(f"send to PC -> {str(msg)}")
            
        except Exception as e:
            print(f"發送區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")
    
    def is_valid_format(self, check_string):
        # 正則表達式:判斷是否匹配格式
        pattern = r'^(\b[0-9A-Fa-f]{2}\b\s*)+$'
        return re.match(pattern, check_string) is not None
    
    def process_list(self, msg_list):
        index0 = msg_list[0]
        print(f"type:{type(index0)}, word:{index0}")
        
        if(index0 == 1):
            pass
        elif(index0 == 2):
            pass
        elif(index0 == 3):
            pass
        elif(index0 == 4):
            index1 = msg_list[1]
            if(index1 == 0):
                self.dev_manager.get_camera_control_instance().turn_right()
            elif(index1 == 1):
                self.dev_manager.get_camera_control_instance().turn_left()
 
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
