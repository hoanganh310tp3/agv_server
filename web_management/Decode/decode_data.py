from django.shortcuts import render
from agv_management.models import AGVData, AGVError
# from PythonWeb.Database import DBInsert
from agv_management.active_agv import is_agv_active


def decodeThis(topic, payload):
    topicName = topic.split("/")[0]
    carID = topic.split("/")[1]

    if topicName == 'AGVData' and is_agv_active(carID):
        deal_with_agv_data(payload)

    if topicName == 'AGVError':
        deal_with_agv_error(payload)

    if topicName == 'AGVHi':
        deal_with_agv_hi(carID)

# def decodeAGVData(payload):
#     Data = AGVData(payload)
#     Data.decodeBuffer()
#     if Data.check_sum():
#         DBInsert.insertAGVData(Data)
#     else:
#         pass


# below code is still used but not in use

def deal_with_agv_data(payload):
    Data = AGVData(payload)
    Data.decodeBuffer()
    DBInsert.insertAGVData(Data)

def deal_with_agv_error(payload):
    error = AGVError(payload)
    error.decodeBuffer()
    DBInsert.insertAGVError(error)

def deal_with_agv_hi(carID):
    pass