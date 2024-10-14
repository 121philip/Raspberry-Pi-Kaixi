import json
import paho.mqtt.client as mqtt
import time
import csv
import sys


"""
parameters
"""
connected = False
Messagerreceived = False
broker = "136.144.226.85"
port = 8884
user = "imp"
password = "testmqtt"
Message = []


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("client is not connected")


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))
    payload = json.loads(message.payload)
    # print(Message)
    Message.append([payload["distance"], payload["led"]])


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


"""
main programs
"""
client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.connect(broker, port=port)
# client.disconnect()
client.loop_start()
client.subscribe("distance_C4")


filename = "distance_data.csv"
while not connected:
    time.sleep(0.2)
while not Messagerreceived:
    time.sleep(0.2)
    if len(Message) > 1:
        with open(filename, "w", newline="") as csvfile:  # using newline="" to avoid empty rows
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(Message)
        csvfile.close()
    sys.exit()
# client.loop_stop()
client.loop_forever()

