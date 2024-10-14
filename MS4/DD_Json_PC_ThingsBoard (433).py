import csv
import json
import time

import paho.mqtt.client as mqtt

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


# def on_log(client, userdata, level, buf):
#     print(buf)


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


"""
main programs
"""
client = mqtt.Client("test")  # create new instance
# client.on_log=on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.username_pw_set(username, password)
client.connect(broker, port)  # establish connection


while not client.connected_flag:  # wait in loop
    client.loop()
    time.sleep(1)
time.sleep(3)


"""
read data from csv file and publish data to ThingsBoard
"""
with open('A:\KU Leuven\OneDrive - KU Leuven\EE2\\files\MS4\distance_data1.csv') as f:
    data = dict()
    reader = csv.reader(f)
    for row in reader:
        data["distance"] = row[0]
        data["led"] = row[1]
        data_out = json.dumps(data)  # create JSON object
        print("publish topic", topic, "data out= ", data_out)
        ret = client.publish(topic, data_out, 0)  # publish
        time.sleep(2)
        client.loop()

client.disconnect()
