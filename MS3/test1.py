import paho.mqtt.client as mqtt
import time
import json

brokers_out = {"broker1": "136.144.226.85",
               "broker2": "imp",
               "broker3": "testmqtt"
               }
print(brokers_out)
print("brokers_out is a ", type(brokers_out))
print("broker 1 address = ", brokers_out["broker1"])
data_out = json.dumps(brokers_out)  # encode object to JSON
print("\nConverting to JSON\n")
print("data-type: ", type(data_out))
print("data out =", data_out)

# At Receiver
print("\nReceived Data\n")
data_in = data_out
print("\ndata in-type ", type(data_in))
print("data in=", data_in)
brokers_in = json.loads(data_in)  # convert incoming JSON to object
print("brokers_in is a ", type(brokers_in))
print("\n\nbroker 2 address = ", brokers_in["broker2"])
cont = input("enter to Continue")


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("data Received type", type(m_decode))
    print("data Received", m_decode)
    print("Converting from Json to Object")
    m_in = json.loads(m_decode)
    print(type(m_in))
    print("broker 2 address = ", m_in["broker2"])


topic = "test/json_test"
client = mqtt.Client("pythontest1")
client.on_message = on_message
print("Connecting to broker ", brokers_out["broker2"])
client.connect(brokers_out["broker1"])
client.loop_start()
client.subscribe(topic)
time.sleep(1)
print("sending data")
client.publish(topic, data_out)
time.sleep(1)
client.loop_stop()
client.disconnect()
