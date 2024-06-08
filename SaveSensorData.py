import os
import threading
import time

from datetime import datetime

class SaveSensorData: # 儲存感測器資料的類別
    def run(self):
        while(True):
            today_date_str = datetime.now().strftime("%Y-%m-%d") # 獲取當前日期
            directory = "/home/pi/AquaPilotFarm/SensorDataLog"  # 設定儲存目錄
            file_name = f"{today_date_str}.txt" # 設定檔案名稱
            file_path = os.path.join(directory, file_name) # 組合目錄和檔案名稱
            os.makedirs(directory, exist_ok=True) # 確定目錄存在，如果不存在就創建
            
            air_temperature = self.air_temp_and_hum_sensor.temperature
            air_humidity = self.air_temp_and_hum_sensor.humidity
            water_temperature = self.water_temp_and_DO_sensor.water_temperature
            water_DO = self.water_temp_and_DO_sensor.DO

            with open(file_path, "a") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, AirTemperature: {air_temperature}C, AirHumidity: {air_humidity}%, WaterTemperature: {water_temperature}C, WaterDO: {water_DO}mg/L \n")
            
            time.sleep(60)

    def __init__(self, air_temp_and_hum_sensor, water_temp_and_DO_sensor):
        self.air_temp_and_hum_sensor = air_temp_and_hum_sensor
        self.water_temp_and_DO_sensor = water_temp_and_DO_sensor

        run = threading.Thread(target = self.run, daemon=True)
        run.start()