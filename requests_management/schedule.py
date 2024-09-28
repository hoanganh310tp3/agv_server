import Dal.schedule
import ABC_algorithm.convert
import ABC_algorithm.schedule
import ABC_algorithm.requirement
from web_management.mqtt import publishMsg
from web_management.Database.DB_insert import insertOrder
from agv_management.active_agv import list_available_AGV
from .models import order_data
from .models import schedule_data
import json
import datetime
import time
import sched
from threading import Thread


def create_schedule():
    ABC_algorithm.schedule.Schedule.ListOfSchedule = list()
    ABC_algorithm.schedule.Schedule.returnListOfSchedule()
    ABC_algorithm.schedule.Schedule.SaveSchedule()
    for EachScheduleIndex, EachSchedule in enumerate(ABC_algorithm.schedule.Schedule.ListOfSchedule):# may be wrong because we mix 2 schedule.py 
        insertOrder(EachSchedule)

def get_control_signal_bytes(ListOfControlSignal):
    frameLength = 0
    ListOfByteControlSignal = bytearray()
    tempByteArray = bytearray()
    ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(122,1)
    for EachControlSignal in range(1, len(ListOfControlSignal)):
        frameLength += 6
        tempByteArray = tempByteArray + ABC_algorithm.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][0],2) + ABC_algorithm.convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][2],1) + ABC_algorithm.convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][3],2) + ABC_algorithm.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][4],1)
    ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(frameLength+4,1) + ABC_algorithm.convert.Convert.returnIntToByte(3,1) + tempByteArray + ABC_algorithm.convert.Convert.returnIntToByte(127,1)
    return ListOfByteControlSignal

def get_sched_for_car():
    now = datetime.datetime.now()
    date = now.date()

    listOfSchedule = list()

    query = schedule_data.objects.filter(order_date = date).values_list('order_date', 'start_time', 'control_signal').order_by('order_date')
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
        topic = "AGVRoute/{Id}".format(Id = normal[0]) # topic may be from mqtt topic
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
    orderQuerySet = order_data.objects.filter(order_date = date, order_number = orderNum).last()

    order = list()
    Requirement = ABC_algorithm.requirement.Requirement()
    Requirement.Order = int(orderQuerySet.order_number)
    Requirement.Name = str(orderQuerySet.load_name)
    Requirement.Number = int(orderQuerySet.load_amount)
    Requirement.LoadWeight = float(orderQuerySet.load_weight)
    Requirement.TimeStart = str(orderQuerySet.start_time)
    Requirement.Inbound = int(orderQuerySet.from_node)
    Requirement.Outbound = int(orderQuerySet.to_node)
    order.append(Requirement)

    ABC_algorithm.schedule.Schedule.reschedule_agv(order)