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

import csv
import json
import sys
import threading
import time

import paho.mqtt.client as mqtt

"""
parameters
"""
clients = [
    {"broker": "136.144.226.85", "port": 8884, "name": "imp", "password": "testmqtt", "sub_topic": "Water Tank",
     "pub_topic": "Water Tank"},
    {"broker": "demo.thingsboard.io", "port": 1883, "name": "5EKbW9hGmeFANF9Brf2p", "password": "",
     "sub_topic": "v1/devices/me/telemetry", "pub_topic": "v1/devices/me/telemetry"}
]
nclients = len(clients)
mqtt.Client.connected_flag = False  # create flag in class

Message = []  # the data which will be put into the csv file


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        for i in range(nclients):
            if clients[i]["client"] == client:
                topic = clients[i]["sub_topic"]
                break
        client.subscribe(topic)
    else:
        print("Bad connection Returned code=", rc)
        client.loop_stop()


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


def on_message(client, userdata, message):
    time.sleep(1)
    print("Message received: " + str(message.payload.decode("utf-8")))
    payload = json.loads(message.payload)
    Message.append([payload["Water Level"], payload["Refill Status"]])


def on_publish(client, userdata, mid):
    time.sleep(1)
    print("In on_pub callback mid= ", mid)


def Create_connections():
    """
    main connecting functions
    """
    for j in range(nclients):
        cname = "client" + str(j)
        t = int(time.time())
        client_id = cname + str(t)  # create unique client_id
        client = mqtt.Client(client_id)  # create new instance
        clients[j]["client"] = client
        clients[j]["client_id"] = client_id
        clients[j]["cname"] = cname
        broker = clients[j]["broker"]
        port = clients[j]["port"]

        client.username_pw_set(clients[j]["name"], clients[j]["password"])
        try:
            client.connect(broker, port)  # establish connection
        except:
            print("Connection Failed to broker ", broker)
            continue

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish
        client.on_message = on_message
        client.loop_start()
        while not client.connected_flag:
            time.sleep(2)


"""
inspect the active client before connecting
"""
no_threads = threading.active_count()
print("current threads =", no_threads)
print("Creating  Connections ", nclients, " clients")

# use this function to create 2 clients
Create_connections()
print("All clients connected ")
time.sleep(5)

"""
inspect the active client after connecting
"""
no_threads = threading.active_count()
print("current threads =", no_threads)

"""
using my PC to subscribe data and publishing the data to ThingsBoard (step 1 and step 3)
"""


def PC_publishing_to_ThingsBoard():
    client = clients[1]["client"]
    pub_topic = clients[1]["pub_topic"]
    with open('A:\KU Leuven\OneDrive - KU Leuven\EE2\\files\MS4\distance_data1.csv') as f:
        data = dict()
        reader = csv.reader(f)
        for row in reader:
            data["Water Level"] = row[0]
            data["Refill Status"] = row[1]
            data_out = json.dumps(data)  # create JSON object
            print("publish topic", pub_topic, "data out= ", data_out)
            ret = client.publish(pub_topic, data_out)  # publish
            time.sleep(2)
            # client.loop()


def PC_subscribing():
    filename = "distance_data1.csv"
    print("subscribing")
    try:
        client = clients[0]["client"]
        sub_topic = clients[0]["sub_topic"]
        client.subscribe(sub_topic)
        while True:
            time.sleep(0.2)
            if len(Message) >= 20:
                with open(filename, "w", newline="") as csvfile:  # using newline="" to avoid empty rows
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(Message)
                csvfile.close()
                break
            # sys.exit()
        # client.loop_stop()
    except KeyboardInterrupt:
        print("interrupted  by keyboard")


PC_subscribing()
PC_publishing_to_ThingsBoard()
