import paho.mqtt.client as mqtt
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_management.settings")


def subcribe():
    client.subscribe("AGV_Data/#")
    client.subscribe("AGVError/#")
    client.subscribe("AGVHi/#")

def publishMsg(pubTopic, pubPayload):
    client.publish(topic= pubTopic, payload= pubPayload)
    
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_connect(client, userdata, flags, rc):
    print('Connect to mosquitto broker successfully')
    client.publish("ConAck", payload="Connected", qos=0, retain=False)
    subcribe()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic} with payload {msg.payload}")
    client.publish("MessageAck", payload="Message received", qos=0, retain=False)
    from web_management.Decode.decode_data import decodeThis  # Move the import here
    decodeThis(msg.topic, msg.payload)

def on_disconnect(client, userdata, rc=0):
    client.loop_stop() 
    
def on_log(client, userdata, level, string): 
    print(string)
    
def start_mqtt_client():
    client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    client.loop_start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

try:
    client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    client.loop_start()
except ValueError as e:
    print(f"Error connecting to MQTT broker: {e}")

