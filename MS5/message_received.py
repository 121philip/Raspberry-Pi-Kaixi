import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "your_broker_address"
MQTT_TOPIC = "your_topic"

client = mqtt.Client()


def on_message(client, userdata, message):
    # Parse the JSON data from the message
    data = json.loads(message.payload.decode("utf-8"))
    # Print the data to the console
    print(data)


client.on_message = on_message
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC)
client.loop_start()
