from django.shortcuts import render
from agv_management.models import AGVData, AGVError, AGVHi
from web_management.Database import DB_insert
from agv_management.active_agv import is_agv_active


def decodeThis(topic, payload):
    print(f"Decoding message from topic {topic} with payload {payload}")
    topicName = topic.split("/")[0].lower()  # Convert to lowercase
    carID = int(topic.split("/")[1])  # Lấy carID từ topic
    print(f"Topic name: {topicName}, Car ID: {carID}")

    if topicName == 'agv_data':
        print("Calling deal_with_agv_data")
        deal_with_agv_data(payload)
    elif topicName == 'agverror':
        deal_with_agv_error(payload)
    elif topicName == 'agv_identify':
        deal_with_agv_identify(payload, carID)  # Truyền thêm carID
    else:
        print(f"Unhandled topic name: {topicName}")

def deal_with_agv_data(payload):
    print(f"Processing AGV data with payload {payload}")
    try:
        Data = AGVData(payload)
        Data.decodeBuffer()
        print(f"Decoded AGV data: {vars(Data)}")
        DB_insert.insertAGVData(Data)
        print("AGV data inserted into database")
    except Exception as e:
        print(f"Error processing AGV data: {e}")

        
def deal_with_agv_error(payload):
    print(f"Processing AGV error with payload {payload}")
    try:
        Data = AGVError(payload)
        Data.decodeBuffer()
        print(f"Decoded AGV error: {vars(Data)}")
        DB_insert.insertAGVError(Data)
        print("AGV error inserted into database")
    except Exception as e:
        print(f"Error processing AGV error: {e}")

def deal_with_agv_identify(payload, carID):
    print(f"Processing AGV identify with payload {payload}")
    try:
        Data = AGVHi(payload)
        Data.decodeBuffer()
        print(f"Decoded AGV identify: {vars(Data)}")
        DB_insert.insertAGVIdentify(Data, carID)  # Truyền thêm carID
        print("AGV identify inserted into database")
    except Exception as e:
        print(f"Error processing AGV identify: {e}")
