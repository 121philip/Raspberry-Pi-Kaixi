import time
from grove.grove_relay import GroveRelay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import csv
from grove.factory import Factory
from grove.display.jhd1802 import JHD1802
import matplotlib.pyplot as plt
from grove.button import Button
from grove.grove_ryb_led_button import GroveLedButton
import paho.mqtt.client as mqtt
import json
import sys

"""
parameters
"""
broker = "demo.thingsboard.io"
port = 1883
topic = "v1/devices/me/telemetry"
username = "5EKbW9hGmeFANF9Brf2p"
password = ""
mqtt.Client.connected_flag = False  # create flag in class
mqtt.Client.suppress_puback_flag = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)
        client.loop_stop()


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


def Data_read_write():
    ax, ay = [], []
    plt.ion()  # open an interaction window

    # Grove - Ultrasonic Ranger connected to port D5
    sensor = GroveUltrasonicRanger(5)
    # Grove - Relay connected to port D16
    relay = GroveRelay(16)
    # Grove - buzzer connected to PWM
    buzzer = Factory.getGpioWrapper("Buzzer", 12)
    # Grove - 16x2 LCD(White on Blue) connected to I2C port
    lcd = JHD1802()
    # Grove - LED Button connected to port D18
    button = GroveLedButton(18)

    f = open('distance_data.csv', 'w', encoding='utf-8')
    csv_write = csv.writer(f)
    header = ['Distance']
    csv_write.writerow(header)

    for i in range(40):
        plt.clf()  # clear the current figure

        distance = sensor.get_distance()
        lcd.setCursor(0, 0)
        lcd.write('distance: {0:2}cm'.format(distance))

        # print('{} cm'.format(distance))
        csv_write.writerow([distance])

        # the dynamic graph
        ax.append(i)
        ay.append([distance])
        plt.plot(ax, ay)
        plt.pause(0.4)

        if distance < 5:
            button.led.light(True)
            relay.on()
            buzzer.on()
            print('relay on, buzzer on')
            time.sleep(0.5)
            relay.off()
            buzzer.off()
            button.led.light(False)
            print('relay off, buzzer off')
            continue
        time.sleep(0.5)
        position = {
            "distance": distance,
            "led": "True",
        }
        jout = json.dumps(position)
        print("data: ", jout)
        client.publish("distance_C4", jout)
    plt.ioff()  # 关闭画图的窗口，即关闭交互模式
    plt.show()  # 显示图片，防止闪退
    f.close()


"""
main programs
"""
client = mqtt.Client("test")  # create new instance
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.username_pw_set(username, password)
client.connect(broker, port)  # establish connection

Data_read_write()
client.disconnect()
