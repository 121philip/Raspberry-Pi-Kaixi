import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "your_broker_address"
MQTT_TOPIC = "your_topic"

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    # Publish the data to the specified topic
    client.publish(MQTT_TOPIC, json.dumps(your_data))


client.on_connect = on_connect
client.connect(MQTT_BROKER)
client.loop_start()
