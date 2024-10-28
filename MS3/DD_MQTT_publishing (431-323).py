"""
Our final goal is doing everything at the same time.
1. use MQTT to publish data from Pi to our PC
2. use our PC to subscribe data through MQTT and save data into csv file
3. publish data to ThingsBoard and observe it

The subscribing part is independent of the publishing part, so you can choose whether execute step 2 or not.
If we want to subscribe and save data into csv file while publishing, we should run "DD_MQTT_subscribing (432-324)"
program when running this program.
But we should combine step 1 and step 3 together since we need to publish real-time data using MQTT and to ThingsBoard.
"""

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
import ssl


"""
parameters
"""
BROKER_ADDRESS = "set-p-gt-01-mqtt.bm.icts.kuleuven.be"
PORT = 1883
USERNAME = "ee2-all"
PASSWORD = "ee2-all"
conn_flag = False


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
            # continue
        time.sleep(0.5)
        position = {
            "distance": distance,
            "led": "True" if distance < 5 else "False",
        }
        jout = json.dumps(position)
        print("data: ", jout)
        client.publish("distance_KAIXI", jout)
    plt.ioff()  # 关闭画图的窗口，即关闭交互模式
    plt.show()  # 显示图片，防止闪退
    f.close()


def on_connect(client, userdata, flags, rc):
    global conn_flag
    conn_flag = True
    print("connected", conn_flag)
    conn_flag = True


def on_log(client, userdata, level, buf):
    print("buffer ", buf)


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        process_message(client, m_decode, topic)
    except:
        print("Error Message Received ")


def process_message(client, msg, topic):
    tnow = time.time()
    print("message =", msg, "Topic ", topic)


"""
main programs
"""
client = mqtt.Client()  # create client object

# Set TLS parameters for a secure connection
client.tls_set(
    ca_certs="/home/pi/Raspberry-Pi-Kaixi/ca 1.crt",
    # Path to the CA certificate file
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)


client.username_pw_set(USERNAME, password=PASSWORD)
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(BROKER_ADDRESS, PORT)  # establish connection


time_wait = 0
while not conn_flag:
    time.sleep(1)
    print("waiting", conn_flag)
    client.loop()
    time_wait += 1
    if time_wait > 6:
        sys.exit(1)
time.sleep(3)

Data_read_write()
