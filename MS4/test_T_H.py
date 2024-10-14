import time

import paho.mqtt.client as paho

ACCESS_TOKEN = '8qJK8FCniEwQgP6ku6X3'  # Token of your device
broker = "demo.thingsboard.io"  # host name
port = 1883  # data listening port


def on_publish(client, userdata, result):  # create function for callback
    print('data published to thingsboard \n')
    pass


client1 = paho.Client('control1')
client1.on_publish = on_publish
client1.username_pw_set(ACCESS_TOKEN)  # access token from thingsboard device
client1.connect(broker, port, keepalive=60)  # establish connection

while True:
    payload = "{"
    payload += "\"Humidity\":60,"
    payload += "\"Temperature\":25"
    payload += "}"
    ret = client1.publish("v1/devices/me/telemetry", payload)  # topic-v1/devices/me/telemetry
    print("Please check LATEST TELEMETRY field of your device")
    print(payload)
    time.sleep(5)
