from django.shortcuts import render
from agv_management.models import AGVData, AGVError
from web_management.Database import DB_insert
from agv_management.active_agv import is_agv_active


def decodeThis(topic, payload):
    print(f"Decoding message from topic {topic} with payload {payload}")
    topicName = topic.split("/")[0].lower()  # Convert to lowercase
    carID = topic.split("/")[1]
    print(f"Topic name: {topicName}, Car ID: {carID}")

    if topicName == 'agv_data':
        print("Calling deal_with_agv_data")
        deal_with_agv_data(payload)
    elif topicName == 'agverror':
        deal_with_agv_error(payload)
    elif topicName == 'agvhi':
        deal_with_agv_hi(carID)
    else:
        print(f"Unhandled topic name: {topicName}")

# def decodeAGVData(payload):
#     Data = AGVData(payload)
#     Data.decodeBuffer()
#     if Data.check_sum():
#         DBInsert.insertAGVData(Data)
#     else:
#         pass


#old code
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

# def deal_with_agv_data(payload):
#     print(f"Processing AGV data with payload {payload}")
#     try:
#         Data = AGVData(payload)
#         Data.decodeBuffer()
#         calculated_checksum = sum(Data.bufferAGVData[1:17]) & 0xFFFF
#         print(f"Calculated checksum: {calculated_checksum}, Received checksum: {Data.checkSum}")
#         print(f"Decoded AGV data: {Data}")
#         if Data.check_sum():
#             DB_insert.insertAGVData(Data)
#             print("AGV data inserted into database")
#         else:
#             print("Checksum validation failed. Data not inserted.")
#         print(f"Raw buffer data: {' '.join([f'{b:02X}' for b in Data.bufferAGVData])}")
#     except Exception as e:
#         print(f"Error processing AGV data: {e}")
#         import traceback
#         print(traceback.format_exc())
        
def deal_with_agv_error(payload):
    error = AGVError(payload)
    error.decodeBuffer()
    DB_insert.insertAGVError(error)

def deal_with_agv_hi(carID):
    pass