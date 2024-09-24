from agv_management.models import agv_data, agv_error
from requests_management.models import schedule_data, order_data

from django.utils import timezone
import json

def insertAGVData(AGVData):
    agv_data.objects.create(  car_id = AGVData.carID, 
                              agv_state = AGVData.carState, 
                              agv_battery= AGVData.carBatteryCap/100, 
                              agv_speed = AGVData.carSpeed/100, 
                              previous_waypoint = AGVData.carPosition.prevNode, 
                              next_waypoint = AGVData.carPosition.nextNode, 
                              distance = AGVData.carPosition.distance/100, 
                              battery_consumption = AGVData.energySum, 
                              distance_sum = AGVData.distanceSum/100,
                              time_stamp = timezone.now())
    
def insertAGVError(AGVError):
    agv_error.objects.create(  car_id = AGVError.carID,
                               order_number = AGVError.orderNum,
                               error_id = AGVError.errorCode,
                               previous_waypoint = AGVError.prevNode, 
                               next_waypoint = AGVError.nextNode)
    
def insertOrder(Order):
    query = schedule_data.objects.filter(order_number = Order.Order, order_date = Order.Date)
    if query:
        query.delete()
    else:
        pass
    schedule_data.objects.create(order_number = Order.Order,
                                load_name = Order.Name,
                                load_weight = Order.LoadWeight,
                                order_date = Order.Date,
                                agv_id = Order.get_car_id(),
                                battery_loss = Order.TotalEnergy, #maybe wrong
                                total_trip = Order.get_total_distance(),
                                start_time = Order.TimeStart,
                                end_time = Order.TimeEnd,
                                begin_waypoint = Order.Inbound,
                                end_waypoint = Order.Outbound,
                                control_signal = json.dumps(Order.list_control_signal()))
    
    order_data.objects.filter(order_number = Order.Order).update(process_status = True)
    
    
