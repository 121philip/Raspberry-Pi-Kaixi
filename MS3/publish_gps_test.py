import json
import random
import sys
import time

import paho.mqtt.client as paho

broker = "136.144.226.85"
port = 8884
user = "imp"
password = "testmqtt"
conn_flag = False


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


client = paho.Client()  # create client object
client.username_pw_set(user, password=password)
# client= paho.Client("control1",transport='websockets')
client.on_log = on_log
# client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(broker, port)  # establish connection
time_wait = 0
while not conn_flag:
    time.sleep(1)
    print("waiting", conn_flag)
    client.loop()
    time_wait += 1
    if time_wait > 6:
        sys.exit(1)
time.sleep(3)
postion = {
    "lat": 54.04558137635778,
    "long": 10.67632251771973
}
slat = 54.04558137635778
slong = 10.67632251771973
print("publishing on port ", port)

time.sleep(6)
count = 0
while count < 100:
    offset = random.random()
    lat = slat + offset
    offset = random.random()
    long = slong + offset
    now = time.time()
    position = {
        "lat": lat,
        "long": long,
        "time": now
    }
    jout = json.dumps(position)
    print("data ", jout)
    client.publish("position", jout)
    count += 1
    time.sleep(1)
client.loop()
time.sleep(2)
client.disconnect()

# https://answers.launchpad.net/mosquitto/+question/260828
