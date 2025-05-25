from agv_management.models import agv_data, agv_error, agv_identify
from requests_management.models import schedule_data, order_data

from django.utils import timezone
import json

def insertAGVData(AGVData, carID):
    agv_data.objects.create(  car_id = carID, 
                              agv_state = AGVData.carState, 
                              agv_battery= AGVData.carBatteryCap/100, 
                              agv_speed = AGVData.carSpeed/100, 
                              previous_waypoint = AGVData.carPosition.prevNode, 
                              next_waypoint = AGVData.carPosition.nextNode, 
                              distance = AGVData.carPosition.distance/100, 
                              distance_sum = AGVData.distanceSum/100,
                              time_stamp = timezone.now())
    
def insertAGVError(AGVError, carID):
    agv_error.objects.create(  car_id = carID,
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
    
def insertOrder(Order):
    """
    Inserts a schedule for an order into the database.
    Validates all required attributes before attempting to create the database entry.
    
    Args:
        Order: A Schedule object containing order data
        
    Returns:
        bool: True if the insertion was successful, False otherwise
        
    Raises:
        AttributeError: If a required attribute is missing
    """
    if Order is None:
        raise AttributeError("Cannot insert None order")
        
    # Validate all required attributes first
    required_attrs = ['Order', 'Name', 'LoadWeight', 'Date', 'TimeStart', 
                      'TimeEnd', 'Inbound', 'Outbound']
    
    for attr in required_attrs:
        if not hasattr(Order, attr) or getattr(Order, attr) is None:
            raise AttributeError(f"Order is missing required attribute: {attr}")
    
    try:
        # Make sure car_id is available
        car_id = Order.get_car_id()
        if car_id is None or car_id == "":
            raise AttributeError("Order has no valid car_id")
            
        # Try to generate control signals
        instruction_set = json.dumps(Order.list_control_signal())
            
        # Create a new schedule entry
        new_schedule = schedule_data.objects.create(
            order_number=Order.Order,
            load_name=Order.Name,
            load_weight=Order.LoadWeight,
            load_amount=Order.LoadAmount,
            order_date=Order.Date,
            agv_id=car_id,
            est_energy=Order.TotalEnergy, 
            est_distance=Order.get_total_distance(),
            est_start_time=Order.TimeStart,
            est_end_time=Order.TimeEnd,
            start_point=Order.Inbound,
            end_point=Order.Outbound,
            instruction_set=instruction_set
        )
        
        # Update the order to mark it as scheduled
        updated_count = order_data.objects.filter(order_number=Order.Order).update(is_scheduled=True)
        
        return True
        
    except Exception as e:
        # Re-raise the exception so the caller can handle it
        raise Exception(f"Error inserting order {getattr(Order, 'Order', 'unknown')}: {str(e)}")
    
    