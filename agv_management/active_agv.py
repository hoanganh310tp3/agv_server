from django.utils import timezone
import datetime
import time

from agv_management.models import agv_data, agv_identify 

def is_agv_active(carID):
    AGVisActive = agv_identify.objects.filter(agv_id = carID, operation = True, connection = True).exists()
    return AGVisActive

def list_active_AGV():
    listOfActiveAGV = []
    AGVisActive = agv_identify.objects.all().filter(operation = True, connection = True).order_by('agv_id')
    for eachQuery in AGVisActive:
        listOfActiveAGV.append([eachQuery.agv_id, eachQuery.parking_lot])
    return listOfActiveAGV

def check_connect_AGV():
    now = time.mktime(datetime.datetime.now().timetuple)

    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar[0]).last()
        dataTime = time.mktime(query.time_stamp.timetuple())
        if (now - dataTime) > 300:
            agv_identify.objects.filter(agv_id = eachCar[0]).update(connected = False)

# may be needed to fix

def list_AGV():
    listOfAGV = []
    AGVisActive = agv_identify.objects.all().order_by('agv_id')
    for eachQuery in AGVisActive:
        listOfAGV.append(eachQuery.agv_id)
    return listOfAGV


def list_available_AGV():
    listOfAvailableAGV = []
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        AGVisAvailable = agv_data.objects.all().filter(car_state__in = [1, 7], agv_id = eachCar).last()
        if AGVisAvailable:
            listOfAvailableAGV.append([AGVisAvailable.car_id.agv_id, AGVisAvailable.previous_waypoint, AGVisAvailable.next_waypoint])
    return listOfAvailableAGV

def check_connect_AGV():
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar[0], car_state = 11).last()
        if query:
            agv_identify.objects.filter(agv_id = eachCar[0]).update(connected = False)
    pass

def deactivate_AGV():
    timeNow = timezone.now()
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar).last()
        if query and (timeNow - query.time_stamp).total_seconds() >= 180:
            agv_identify.objects.filter(agv_id = eachCar).update(is_active = False)

