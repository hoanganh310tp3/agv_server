from django.shortcuts import render
from django.http import HttpResponse
import ABC_algorithm.schedule
import Dal.data_frame.send
from requests_management.schedule import schedule_agv
from web_management.mqtt import publishMsg
from web_management.Database.DB_insert import insertOrder


# Create your views here.
# def Index(Request):
#         create_schedule()
#         latestSchedule = get_latest_schedule()

#         Response = HttpResponse()
        
#         for EachSchedule in Dto.Schedule.Schedule.ListOfSchedule:
#             Response.write(EachSchedule.SendToUI())

#         for eachSchedule in latestSchedule:
#             topic = "Server/{Id}".format(Id = eachSchedule[0])
#             publishMsg(topic, get_control_signal_bytes(eachSchedule))
#             # print(get_control_signal_bytes(eachSchedule))
#             # print(eachSchedule)
            
#         return Response

def Index(Request):
        schedule_agv()        
        Response = HttpResponse("Schedule created successfully!")

        return Response
