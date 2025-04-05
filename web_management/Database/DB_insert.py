from agv_management.models import agv_data, agv_error, agv_identify
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
                              distance_sum = AGVData.distanceSum/100,
                              time_stamp = timezone.now())
    
def insertAGVError(AGVError):
    agv_error.objects.create(  car_id = AGVError.carID,
                               order_number = AGVError.orderNum,
                               error_id = AGVError.errorCode,
                               previous_waypoint = AGVError.prevNode, 
                               next_waypoint = AGVError.nextNode)
    
def insertAGVIdentify(AGVIdentify, carID):
    is_active_bool = AGVIdentify.isActive == 1
    is_connected_bool = AGVIdentify.isConnected == 1
    
    guidance_type_map = {
        1: 'line_following',
        2: 'image_processing'
    }
    guidance_type_str = guidance_type_map.get(AGVIdentify.guidanceType, 'line_following')
    
    agv_identify.objects.update_or_create(
        agv_id=carID,
        defaults={
            'max_speed': AGVIdentify.maxSpeed/100,
            'battery_capacity': AGVIdentify.batteryCapacity/100,
            'max_load': AGVIdentify.maxLoad,
            'guidance_type': guidance_type_str,
            'is_active': is_active_bool,
            'is_connected': is_connected_bool,
            'parking_lot': AGVIdentify.parkingLot
        }
    )
    
# def insertOrder(Order):
#     query = schedule_data.objects.filter(order_number = Order.Order, order_date = Order.Date)
#     if query:
#         query.delete()
#     else:
#         pass
#     schedule_data.objects.create(order_number = Order.Order,
#                                 load_name = Order.Name,
#                                 load_weight = Order.LoadWeight,
#                                 load_amount = Order.LoadAmount,
#                                 order_date = Order.Date,
#                                 agv_id = Order.get_car_id(),
#                                 est_energy = Order.TotalEnergy, #maybe wrong
#                                 est_distance = Order.get_total_distance(),
#                                 est_start_time = Order.TimeStart,
#                                 est_end_time = Order.TimeEnd,
#                                 start_point = Order.Inbound,
#                                 end_point = Order.Outbound,
#                                 instruction_set = json.dumps(Order.list_control_signal()))
    
#     order_data.objects.filter(order_number = Order.Order).update(is_scheduled = True)
    

def insertOrder(Order, replace_existing=False):
       # Chỉ xóa lịch cũ nếu replace_existing=True
    if replace_existing:
        query = schedule_data.objects.filter(order_number=Order.Order, order_date=Order.Date)
        if query:
            query.delete()
               
       # Thêm thông tin phiên lập lịch để phân biệt
    schedule_data.objects.create(
        order_number=Order.Order,
        load_name = Order.Name,
        load_weight = Order.LoadWeight,
        load_amount = Order.LoadAmount,
        order_date = Order.Date,
        agv_id = Order.get_car_id(),
        est_energy = Order.TotalEnergy, #maybe wrong
        est_distance = Order.get_total_distance(),
        est_start_time = Order.TimeStart,
        est_end_time = Order.TimeEnd,
        start_point = Order.Inbound,
        end_point = Order.Outbound,
        session_id=timezone.now().strftime("%Y%m%d%H%M%S"),  # Thêm trường mới để phân biệt
        instruction_set=json.dumps(Order.list_control_signal())
       )
    order_data.objects.filter(order_number = Order.Order).update(is_scheduled = True)