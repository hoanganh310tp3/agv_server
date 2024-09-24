import Dal.schedule

import ABC_algorithm.convert

import ABC_algorithm.schedule
import ABC_algorithm.requirement


from web_management.mqtt import publishMsg

from PythonWeb.Database.DBInsert import insertOrder

from ManageAGV.activeAGV import list_available_AGV
from ManageRequests.models import DB_SimpleOrder

import json
import datetime
import time
import sched
from threading import Thread

from .models import DB_Schedule

def create_schedule():
    Dto.Schedule.Schedule.ListOfSchedule = list()
    Bll.Schedule.Schedule.returnListOfSchedule()
    Dal.Schedule.Schedule.SaveSchedule()
    for EachScheduleIndex, EachSchedule in enumerate(Dto.Schedule.Schedule.ListOfSchedule):
        insertOrder(EachSchedule)

def get_control_signal_bytes(ListOfControlSignal):
    frameLength = 0
    ListOfByteControlSignal = bytearray()
    tempByteArray = bytearray()
    ListOfByteControlSignal = ListOfByteControlSignal + Bll.Convert.Convert.returnIntToByte(122,1)
    for EachControlSignal in range(1, len(ListOfControlSignal)):
        frameLength += 6
        tempByteArray = tempByteArray + Bll.Convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][0],2) + Bll.Convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][2],1) + Bll.Convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][3],2) + Bll.Convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][4],1)
    ListOfByteControlSignal = ListOfByteControlSignal + Bll.Convert.Convert.returnIntToByte(frameLength+4,1) + Bll.Convert.Convert.returnIntToByte(3,1) + tempByteArray + Bll.Convert.Convert.returnIntToByte(127,1)
    return ListOfByteControlSignal

def get_sched_for_car():
    now = datetime.datetime.now()
    date = now.date()

    listOfSchedule = list()

    query = DB_Schedule.objects.filter(order_date = date).values_list('order_date', 'start_time', 'control_signal').order_by('order_date')
    if query:
        listOfSchedule = list(query)
    else:
        pass

    return listOfSchedule

def schedule_agv():

    create_schedule()
    latestSchedule = get_sched_for_car()

    scheduler = sched.scheduler(time.time, time.sleep)

    for eachSchedule in latestSchedule:
        normal = json.loads(eachSchedule[2])
        topic = "AGVRoute/{Id}".format(Id = normal[0])
        payload = get_control_signal_bytes(normal)
        timeAt = "{date} {time}".format(date = str(eachSchedule[0]), time = eachSchedule[1])
        scheduler.enterabs(time.mktime(time.strptime(timeAt, "%Y-%m-%d %H:%M:%S")), 0, publishMsg, (topic, payload))

    print(scheduler.queue)
    scheduleThread = Thread(target = threaded_schedule, args = (scheduler, ))
    scheduleThread.start()

def threaded_schedule(scheduler):
    scheduler.run()

def return_to_lot():
    # get current location of agv
    # route plan for location back to parking station:
    pass

def resched_agv(orderNum):
    now = datetime.datetime.now()
    date = now.date()
    orderQuerySet = DB_SimpleOrder.objects.filter(order_date = date, order_number = orderNum).last()

    order = list()
    Requirement = Dto.Requirement.Requirement()
    Requirement.Order = int(orderQuerySet.order_number)
    Requirement.Name = str(orderQuerySet.load_name)
    Requirement.Number = int(orderQuerySet.load_amount)
    Requirement.LoadWeight = float(orderQuerySet.load_weight)
    Requirement.TimeStart = str(orderQuerySet.start_time)
    Requirement.Inbound = int(orderQuerySet.from_node)
    Requirement.Outbound = int(orderQuerySet.to_node)
    order.append(Requirement)

    Bll.Schedule.Schedule.reschedule_agv(order)