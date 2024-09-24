import paho.mqtt.client as mqtt
from django.conf import settings
import os
import django
# from web_management.Decode.decode_data import decodeThis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_management.settings")
django.setup()

def subcribe():
    client.subscribe("AGV_Data/#")
    client.subscribe("AGVError/#")
    client.subscribe("AGVHi/#")

def publishMsg(pubTopic, pubPayload):
    client.publish(topic= pubTopic, payload= pubPayload)
    
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


# def on_connect(mqtt_client, userdata, flags, rc):
#     if rc == 0:
#         print('Connect to mosquitto broker successfully')
#         mqtt_client.subscribe('django/mqtt')
#         subcribe()
#     else:
#         print('Bad connection. Return Code:', rc)

def on_connect(client, userdata, flags, rc):
    print('Connect to mosquitto broker successfully')
    client.publish("ConAck", payload="Connected", qos=0, retain=False)
    subcribe()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# def on_message(client, userdata, msg):
#     client.publish("MessageAck", payload="Message received", qos=0,retain=False)

def on_message(client, userdata, msg):
    client.publish("MessageAck", payload="Message received", qos=0, retain=False)
    decodeThis(msg.topic, msg.payload)

def on_disconnect(client, userdata,rc=0):
    client.loop_stop() 
    
def on_log(client, userdata, level, string): 
    print(string)


client = mqtt.Client()
client.on_connect = on_connect
client.on_subcribe = on_subscribe
client.on_message = on_message
client.connect(
        host=settings.MQTT_SERVER,
        port=settings.MQTT_PORT,
        keepalive=settings.MQTT_KEEPALIVE
    )
