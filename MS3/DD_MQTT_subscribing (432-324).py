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
import ssl

"""
parameters
"""
BROKER_ADDRESS = "set-p-gt-01-mqtt.bm.icts.kuleuven.be"
PORT = 1883
USERNAME = "ee2-all"
PASSWORD = "ee2-all"
TOPIC = "test/topic"
Message = []
filename = "distance_data.csv"


# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to broker")
        # Subscribe to topic upon successful connection
    else:
        print("Connection failed with code {}".format(rc))


# Callback for when a message is received from the server.
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

# Set TLS parameters for a secure connection
client.tls_set(
    ca_certs="A:\OneDrive - KU Leuven\Master\Student Assistant\Raspberry-Pi-Kaixi\ca 1.crt",
    # Path to the CA certificate file
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)

client.on_message = on_message
client.username_pw_set(USERNAME, password=PASSWORD)
client.on_connect = on_connect
client.connect(BROKER_ADDRESS, port=PORT)
# client.disconnect()
# client.loop_start()
client.subscribe("distance_KAIXI")

# while not Messagerreceived:
#     time.sleep(0.2)
#     if len(Message) >= 10:

# sys.exit()
# Blocking loop to process network traffic and dispatch callbacks
client.loop_forever()
