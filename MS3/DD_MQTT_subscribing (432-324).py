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


class MQTTClient:
    def __init__(self, broker_address, port, username, password, topic, filename, ca_cert_path):
        """
        Initialize the MQTT client with broker details, topic, and file path for saving data.
        """
        self.broker_address = broker_address
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.filename = filename
        self.ca_cert_path = ca_cert_path
        self.client = mqtt.Client()
        self.configure_client()

    def configure_client(self):
        """
        Configure the MQTT client with TLS settings, username/password, and callback methods.
        """
        self.client.tls_set(
            ca_certs=self.ca_cert_path,
            # Path to the CA certificate file
            certfile=None,
            keyfile=None,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None
        )
        self.client.username_pw_set(self.username, password=self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for when the client receives a CONNACK response from the server.
        """
        if rc == 0:
            print("Connected successfully to broker")
            # Subscribe to topic upon successful connection
            self.client.subscribe(self.topic)
        else:
            print("Connection failed with code {}".format(rc))

    def on_message(self, client, userdata, message):
        """
        Callback for when a message is received from the server.
        """
        try:
            payload = json.loads(message.payload)
            print("Message received: {}".format(payload))
            print("Topic: {}".format(message.topic))
        except json.JSONDecodeError as e:
            print("Connection failed with code {}".format(e))

    def write_to_csv(self, payload):
        """
        Write the received data to a CSV file.
        """
        try:
            with open(self.filename, "a", newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([payload.get("led", "N/A"), payload.get("distance", "N/A")])
        except IOError as e:
            print("Failed to write to CSV file: {}".format(e))
        csvfile.close()

    def on_disconnect(self, client, userdata, rc):
        """
        Callback for when the client disconnects from the server.
        """
        print("client disconnected ok")

    def on_publish(self, client, userdata, mid):
        """
        Callback for when a message is published to the broker.
        """
        print(f"Message published with mid: {mid}")

    def start(self):
        """
        Start the MQTT client loop to listen for messages.
        """
        self.client.connect(self.broker_address, port=self.port)
        self.client.loop_forever()

if __name__ == "__main__":
    # Configuration Parameters
    BROKER_ADDRESS = "set-p-gt-01-mqtt.bm.icts.kuleuven.be"
    PORT = 1883
    USERNAME = "ee2-all"
    PASSWORD = "ee2-all"
    TOPIC = "distance_KAIXI"
    FILENAME = "distance_data.csv"
    CA_CERT_PATH = "A:\OneDrive - KU Leuven\Master\Student Assistant\Raspberry-Pi-Kaixi\ca 1.crt"

    # Initialize and start the MQTT client
    mqtt_client = MQTTClient(BROKER_ADDRESS, PORT, USERNAME, PASSWORD, TOPIC, FILENAME, CA_CERT_PATH)
    mqtt_client.start()
