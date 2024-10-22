import paho.mqtt.client as mqtt
import ssl
import threading

# MQTT Broker settings
BROKER_ADDRESS = "set-p-gt-01-mqtt.bm.icts.kuleuven.be"
PORT = 1883
USERNAME = "ee2-all"
PASSWORD = "ee2-all"
TOPIC = "test/topic"


# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to broker")
        # Subscribe to topic upon successful connection
    else:
        print("Connection failed with code {}".format(rc))


# Callback for when a message is received from the server.
def on_message(client, userdata, msg):
    print("Received a message on: '{}' on topic '{}'".format(msg.payload.decode(), msg.topic))


# Create MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(USERNAME, PASSWORD)

# Set TLS parameters for a secure connection
client.tls_set(
    ca_certs="A:\OneDrive - KU Leuven\Master\Student Assistant\Raspberry-Pi-Kaixi\ca 1.crt",
    # Path to the CA certificate file
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)

# Enable TLS (Transport Layer Security)
client.tls_insecure_set(False)  # Set to True if the server uses a self-signed certificate

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER_ADDRESS, PORT, 60)


# Function to publish messages in real-time
def publish_realtime():
    while True:
        message = input("Enter the message to publish: ")
        client.publish(TOPIC, message)


# Start a new thread to handle publishing in real-time
publish_thread = threading.Thread(target=publish_realtime)
publish_thread.start()

# Blocking loop to process network traffic and dispatch callbacks
client.loop_forever()
