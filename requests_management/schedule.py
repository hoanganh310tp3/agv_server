import BLL.schedule
import DTO.schedule
import BLL.convert
import Dal.schedule
import DTO.requirement

from web_management.mqtt import publishMsg
from web_management.Database.DB_insert import insertOrder

from agv_management.active_agv import list_available_AGV
from requests_management.models import order_data

import json
import datetime
import time
import sched
from threading import Thread

from .models import schedule_data

import logging
logger = logging.getLogger(__name__)

def create_schedule():
    try:
        logger.info("Starting schedule creation")
        DTO.schedule.Schedule.ListOfSchedule = list()
        BLL.schedule.Schedule.returnListOfSchedule()
        Dal.schedule.Schedule.SaveSchedule()
        for EachScheduleIndex, EachSchedule in enumerate(DTO.schedule.Schedule.ListOfSchedule):
            insertOrder(EachSchedule)
        logger.info("Schedule creation completed successfully")
    except Exception as e:
        logger.error(f"Error creating schedule: {e}")
        raise

def get_control_signal_bytes(ListOfControlSignal):
    frameLength = 0
    ListOfByteControlSignal = bytearray()
    tempByteArray = bytearray()
    ListOfByteControlSignal = ListOfByteControlSignal + BLL.convert.Convert.returnIntToByte(122,1)
    for EachControlSignal in range(1, len(ListOfControlSignal)):
        frameLength += 6
        tempByteArray = tempByteArray + BLL.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][0],2) + BLL.convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][2],1) + BLL.convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][3],2) + BLL.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][4],1)
    ListOfByteControlSignal = ListOfByteControlSignal + BLL.convert.Convert.returnIntToByte(frameLength+4,1) + BLL.convert.Convert.returnIntToByte(3,1) + tempByteArray + BLL.convert.Convert.returnIntToByte(127,1)
    return ListOfByteControlSignal

def get_sched_for_car():
    now = datetime.datetime.now()
    date = now.date()

    listOfSchedule = list()

    query = schedule_data.objects.filter(order_date=date).values_list(
        'order_date', 
        'est_start_time', 
        'instruction_set'
    ).order_by('order_date')
    
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


# Make agv return to parking station but not done

def return_to_lot():
    # get current location of agv
    # route plan for location back to parking station:
    pass

def resched_agv(orderNum):
    now = datetime.datetime.now()
    date = now.date()
    orderQuerySet = order_data.objects.filter(order_date = date, order_number = orderNum).last()

    order = list()
    Requirement = DTO.requirement.Requirement()
    Requirement.Order = int(orderQuerySet.order_number)
    Requirement.Name = str(orderQuerySet.load_name)
    Requirement.Number = int(orderQuerySet.load_amount)
    Requirement.LoadWeight = float(orderQuerySet.load_weight)
    Requirement.TimeStart = str(orderQuerySet.start_time)
    Requirement.Inbound = int(orderQuerySet.from_node)
    Requirement.Outbound = int(orderQuerySet.to_node)
    order.append(Requirement)

    BLL.schedule.Schedule.reschedule_agv(order)