# 引入Adafruit_DHT
import time
import Adafruit_DHT
from seeed_dht import DHT
import csv

# 定义sensor型号为DHT11，引脚为D18
sensor = DHT('11', 18)
filename = "hu_temp.csv"

# start_time = time.time()

f = open('csv_file.csv', 'w', encoding='utf-8')
csv_write = csv.writer(f)

for i in range(10):
    # 读取温湿度数据到temp和hu两个变量中
    hu, temp = sensor.read()
    # 打印出结果
    print('temp:{0:0.1f} hu:{1}'.format(temp, hu))
    data = [temp, hu]
    # writing the fields
    csv_write.writerow(data)
    # 循环延迟设为3秒
    time.sleep(1)

f.close()
