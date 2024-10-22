# 引入Adafruit_DHT
import csv
import time

import matplotlib.pyplot as plt
from seeed_dht import DHT


def data_read_write():
    ax = []
    ay = []
    bx = []
    by = []

    plt.ion()
    # 定义sensor型号为DHT11，引脚为D18
    sensor = DHT('11', 18)

    # start_time = time.time()

    f = open('temperature_humidity.csv', 'w', encoding='utf-8')
    csv_write = csv.writer(f)

    header = ['temperature', 'humidity']
    csv_write.writerow(header)

    for i in range(10):
        plt.clf()  # 清除刷新前的图表，防止数据量过大消耗内存
        # 读取温湿度数据到temp和hu两个变量中
        hu, temp = sensor.read()
        # 打印出结果
        print('temp:{0:0.1f} hu:{1}'.format(temp, hu))
        data = [temp, hu]
        # writing the fields
        csv_write.writerow(data)
        # 循环延迟设为3秒
        time.sleep(1)

        # graph 1
        ax.append(i)
        ay.append([temp])
        agraphic = plt.subplot(2, 1, 1)
        agraphic.plot(ax, ay)

        # graph 2
        bx.append(i)
        by.append([hu])
        bgraphic = plt.subplot(2, 1, 2)
        bgraphic.plot(bx, by)

        plt.pause(0.4)

        i += 1

    plt.ioff()  # 关闭画图的窗口，即关闭交互模式
    plt.show()  # 显示图片，防止闪退

    f.close()


data_read_write()
# def visualize():
#     data = pd.read_csv("csv_file.csv")
#     
# 
#     plt.show()
