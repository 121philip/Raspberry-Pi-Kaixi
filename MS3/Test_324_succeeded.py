import json

import paho.mqtt.client as paho
import time
import psutil

broker_address = "136.144.226.85"
port = 8884
user = "imp"
password = "testmqtt"
conn_flag = False


def on_connect(client, userdata, flags, rc):
    global conn_flag
    conn_flag = True
    print("connected", conn_flag)
    conn_flag = True


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))


def get_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    info = {
        'cpu_percent': cpu_percent,
        'cpu_count': cpu_count,
        'mem_percent': mem_percent,
    }
    return json.dumps(info)


connected = False
Messagerreceived = False


client = paho.Client()
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)
client.loop_start()
client.subscribe("test1_yao")
while not connected:
    time.sleep(0.2)
while not Messagerreceived:
    time.sleep(0.2)

client.loop_stop()
# while True:
#     time.sleep(1)
#     msg = get_info()
#     result = client.publish(msg)
#     status = result[0]
#     if status == 0:
#         print(f"Send {msg}")
#     else:
#         print(f"Failed to send message")
