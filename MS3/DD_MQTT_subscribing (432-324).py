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
filename = "distance_data.csv"


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
    # Message.append([payload["distance"], payload["led"]])
    # csvfile = open(filename, "a")
    with open(filename, "a") as csvfile:  # using newline="" to avoid empty rows
        csvwriter = csv.writer(csvfile)
        print(payload["led"])
        csvwriter.writerow(payload["led"])
    # csvfile.writelines(payload["led"])
    csvfile.close()


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
# client.loop_start()
client.subscribe("distance_C4")

# while not Messagerreceived:
#     time.sleep(0.2)
#     if len(Message) >= 10:

# sys.exit()
client.loop_forever()
