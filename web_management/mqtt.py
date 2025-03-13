import paho.mqtt.client as mqtt
from django.conf import settings
import os
import django
import time
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_management.settings")


def subcribe():
    client.subscribe("AGV_Data/#")
    client.subscribe("AGVError/#")
    client.subscribe("AGV_Identify/#")

def publishMsg(pubTopic, pubPayload):
    try:
        client.publish(topic=pubTopic, payload=pubPayload)
    except Exception as e:
        print(f"Error publishing message: {e}")
        # Thử kết nối lại nếu mất kết nối
        if connect_with_retry(client):
            client.loop_start()
            client.publish(topic=pubTopic, payload=pubPayload)
    
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT broker at {settings.MQTT_SERVER}:{settings.MQTT_PORT}")
        client.publish("ConAck", payload="Connected", qos=0, retain=False)
        subcribe()
    else:
        logger.error(f"Failed to connect to MQTT broker with code: {rc}")
        # Mã lỗi MQTT connection
        rc_codes = {
            1: "Incorrect protocol version",
            2: "Invalid client identifier",
            3: "Server unavailable",
            4: "Bad username or password",
            5: "Not authorized"
        }
        logger.error(f"Error message: {rc_codes.get(rc, 'Unknown error')}")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic} with payload {msg.payload}")
    client.publish("MessageAck", payload="Message received", qos=0, retain=False)
    from web_management.Decode.decode_data import decodeThis  # Move the import here
    decodeThis(msg.topic, msg.payload)

def on_disconnect(client, userdata, rc=0):
    print("Disconnected from MQTT broker")
    client.loop_stop()
    
def on_log(client, userdata, level, string): 
    print(string)

def connect_with_retry(client, max_retries=10, retry_delay=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            logger.info(f"Attempting to connect to MQTT broker at {settings.MQTT_SERVER}:{settings.MQTT_PORT} (Attempt {retry_count + 1}/{max_retries})")
            client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
            return True
        except Exception as e:
            retry_count += 1
            logger.error(f"Failed to connect: {str(e)}")
            if retry_count < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    return False
    
def start_mqtt_client():
    if connect_with_retry(client):
        client.loop_start()
    else:
        print("Could not connect to MQTT broker after maximum retries")

# Khởi tạo client với client ID duy nhất
client_id = f'django-mqtt-{str(uuid.uuid4())}'
client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

# Thêm logging cho debugging
client.on_log = on_log

# Thử kết nối với retry logic
logger.info("Starting MQTT client...")
try:
    if connect_with_retry(client):
        client.loop_start()
        logger.info("MQTT client started successfully")
    else:
        logger.error("Could not connect to MQTT broker after maximum retries")
except Exception as e:
    logger.error(f"Error in MQTT setup: {e}")