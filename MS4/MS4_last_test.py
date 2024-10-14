import json
import time
import paho.mqtt.client as mqtt
import threading
import random

"""
parameters
"""
clients = [
    {"broker": "136.144.226.85", "port": 8884, "name": "imp", "password": "testmqtt", "sub_topic": "test1",
     "pub_topic": "test1"},
    {"broker": "demo.thingsboard.io", "port": 1883, "name": "5EKbW9hGmeFANF9Brf2p", "password": "",
     "sub_topic": "v1/devices/me/telemetry", "pub_topic": "v1/devices/me/telemetry"}
]

nclients = len(clients)
message = "test message"

out_queue = []  # use simple array to get printed messages in some form of order
mqtt.Client.connected_flag = False  # create flag in class


def on_message(client, userdata, message):
    time.sleep(1)
    msg = "message received", str(message.payload.decode("utf-8"))
    print(msg)
    out_queue.append(msg)


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
            time.sleep(0.05)


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
using MQTT to publish the data from my PC and forwarding the data to ThingsBoard
"""


def publishing():
    print("Publishing")
    try:
        while True:
            i = 0
            for i in range(nclients):
                client = clients[i]["client"]
                pub_topic = clients[i]["pub_topic"]

                json_out = data()

                if client.connected_flag:
                    client.publish(pub_topic, json_out)
                    time.sleep(0.1)
                    print("publishing client " + str(i))
                i += 1
            time.sleep(10)  # now print messages
            print("queue length=", len(out_queue))
            for x in range(len(out_queue)):
                print(out_queue.pop())
            # time.sleep(5)#wait

    except KeyboardInterrupt:
        print("interrupted  by keyboard")


def data():
    slat = 54.04558137635778
    slong = 10.67632251771973

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
    print("data" + jout)
    return jout


publishing()
