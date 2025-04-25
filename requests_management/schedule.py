import BLL.schedule
import DTO.schedule
import BLL.convert
import Dal.schedule
import DTO.requirement
import BLL.position
import DTO.agv_car

from web_management.mqtt import publishMsg
from web_management.Database.DB_insert import insertOrder

from agv_management.active_agv import list_available_AGV
from requests_management.models import order_data

import json
import datetime
import time
import sched
from threading import Thread
import asyncio

from .models import schedule_data

import logging
logger = logging.getLogger(__name__)

def create_schedule():
    try:
        logger.info("Starting schedule creation")
        
        # Get current date and time
        now = datetime.datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")
        
        # Check which orders have already been scheduled
        scheduled_orders = set(schedule_data.objects.filter(
            order_date=date
        ).values_list('order_number', flat=True))
        
        logger.info(f"Found {len(scheduled_orders)} already scheduled orders")
        
        # Start with a fresh list for new schedules
        current_schedule_list = DTO.schedule.Schedule.ListOfSchedule.copy() if DTO.schedule.Schedule.ListOfSchedule else []
        DTO.schedule.Schedule.ListOfSchedule = []
        
        # Filter orders:
        # 1. Not already scheduled
        # 2. Not in the past (start time is in the future)
        # 3. Not already completed (is_processed=False)
        unscheduled_orders = order_data.objects.filter(
            order_date=date,
            is_scheduled=False  # Only get unscheduled orders
        ).exclude(
            start_time__lt=current_time  # Exclude orders with start time in the past
        )
        
        if not unscheduled_orders.exists():
            logger.info("No new valid orders to schedule. All orders have either been scheduled or are in the past.")
            return
            
        logger.info(f"Found {unscheduled_orders.count()} unscheduled future orders to process")
        
        # Generate new schedules only for valid future orders
        original_orders = BLL.requirement.Requirement.ReadTimeTable
        
        # Override ReadTimeTable to only return valid future orders
        def filtered_read_time_table():
            orders = []
            for order in unscheduled_orders:
                requirement = DTO.requirement.Requirement()
                requirement.Order = int(order.order_number)
                requirement.Date = str(order.order_date)
                requirement.Name = str(order.load_name)
                requirement.LoadAmount = int(order.load_amount)
                requirement.LoadWeight = float(order.load_weight)
                requirement.TimeStart = str(order.start_time)
                requirement.Inbound = int(order.start_point)
                requirement.Outbound = int(order.end_point)
                orders.append(requirement)
            return orders
            
        # Replace the method temporarily
        BLL.requirement.Requirement.ReadTimeTable = filtered_read_time_table
        
        # Now generate schedules only for valid orders
        BLL.schedule.Schedule.returnListOfSchedule()
        
        # Restore the original method
        BLL.requirement.Requirement.ReadTimeTable = original_orders
        
        # Process and save newly generated schedules
        newly_created = []
        for EachSchedule in DTO.schedule.Schedule.ListOfSchedule:
            # Check if EachSchedule is valid before inserting
            if EachSchedule is None:
                logger.warning("Skipping None schedule object")
                continue
                
            # Validate required fields to prevent AttributeError
            if not hasattr(EachSchedule, 'Order') or EachSchedule.Order is None:
                logger.warning(f"Schedule missing Order attribute - skipping")
                continue
                
            try:
                insertOrder(EachSchedule)
                newly_created.append(EachSchedule)
                logger.info(f"Successfully created schedule for Order #{EachSchedule.Order}")
            except Exception as insert_error:
                logger.error(f"Error inserting order {getattr(EachSchedule, 'Order', 'unknown')}: {insert_error}")
        
        # Save the schedule to CSV
        Dal.schedule.Schedule.SaveSchedule()
        
        logger.info(f"Schedule creation completed successfully. Created {len(newly_created)} new schedules for future orders.")
    except Exception as e:
        logger.error(f"Error creating schedule: {e}")
        raise

def get_control_signal_bytes(ListOfControlSignal):
    frameLength = 0
    ListOfByteControlSignal = bytearray()
    tempByteArray = bytearray()
    ListOfByteControlSignal = ListOfByteControlSignal + BLL.convert.Convert.returnIntToByte(122,1)
    for EachControlSignal in range(1, len(ListOfControlSignal)):
        frameLength += 5 # Increase by 2 to account for waitTime (2 bytes)
        # Include waitTime in the serialized data (converting to float with 2 bytes)
        tempByteArray = tempByteArray + BLL.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][0],2) + BLL.convert.Convert.returnIntToByte(ListOfControlSignal[EachControlSignal][4],1) + BLL.convert.Convert.returnFloatToByte(ListOfControlSignal[EachControlSignal][5] if len(ListOfControlSignal[EachControlSignal]) > 5 else 0, 2)
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
    # Only create schedules for new orders that are still in the future
    create_schedule()
    
    # Get all valid active schedules for today
    now = datetime.datetime.now()
    date = now.date()
    
    # Get schedules that are not marked as completed/processed
    active_schedules = schedule_data.objects.filter(
        order_date=date,
        is_processed=False
    ).values_list(
        'order_date', 
        'est_start_time', 
        'instruction_set',
        'est_end_time'
    ).order_by('est_start_time')
    
    if not active_schedules:
        logger.info("No active schedules found for today")
        return
    
    logger.info(f"Found {len(active_schedules)} active schedules to process")
    
    # Create a scheduler for running the MQTT pub/sub at the right times
    scheduler = sched.scheduler(time.time, time.sleep)
    
    now_timestamp = time.mktime(now.timetuple())
    
    for schedule in active_schedules:
        normal = json.loads(schedule[2])
        topic = f"AGVRoute/{normal[0]}"
        
        # Get the schedule times
        start_time = "{date} {time}".format(date=str(schedule[0]), time=schedule[1])
        end_time = "{date} {time}".format(date=str(schedule[0]), time=schedule[3])
        
        start_timestamp = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        end_timestamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        
        # Skip schedules that are already completed
        if end_timestamp < now_timestamp:
            logger.info(f"Skipping completed schedule for AGV {normal[0]}, ended at {schedule[3]}")
            continue
        
        # For schedules currently in progress or upcoming
        if start_timestamp <= now_timestamp:
            # Schedule is in progress, send immediately with current position
            payload = get_control_signal_bytes(normal)
            logger.info(f"Sending immediate schedule for in-progress AGV {normal[0]}")
            publishMsg(topic, payload)
        else:
            # Schedule for future execution
            payload = get_control_signal_bytes(normal)
            scheduler.enterabs(start_timestamp, 0, publishMsg, (topic, payload))
            logger.info(f"Scheduled for future execution: AGV {normal[0]} at {schedule[1]}")
    
    # Only start thread if there are future scheduled events
    if scheduler.queue:
        logger.info(f"Starting scheduler thread with {len(scheduler.queue)} events")
        print(scheduler.queue)
        scheduleThread = Thread(target=threaded_schedule, args=(scheduler,))
        scheduleThread.start()
    else:
        logger.info("No future schedules to process")

def threaded_schedule(scheduler):
    scheduler.run()


# Make agv return to parking station but not done

def return_to_lot():
    # get current location of agv
    # route plan for location back to parking station:
    pass

def resched_agv(orderNum):
    """
    Reschedules a specific order by order number, but only if the order
    is not in the past and not already completed.
    """
    try:
        now = datetime.datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")
        
        # Get the order, ensuring it's not in the past
        orderQuerySet = order_data.objects.filter(
            order_date=date, 
            order_number=orderNum,
            start_time__gte=current_time  # Only future orders
        ).last()
        
        if not orderQuerySet:
            logger.warning(f"Order #{orderNum} not found or is in the past - cannot reschedule")
            return False
            
        # Check if there's already a schedule for this order
        existing_schedule = schedule_data.objects.filter(
            order_date=date,
            order_number=orderNum,
            is_processed=False
        ).first()
        
        if existing_schedule:
            # Delete existing schedule first
            existing_schedule.delete()
            logger.info(f"Deleted existing schedule for order #{orderNum}")
        
        # Create requirement from order
        order = list()
        Requirement = DTO.requirement.Requirement()
        Requirement.Order = int(orderQuerySet.order_number)
        Requirement.Name = str(orderQuerySet.load_name)
        Requirement.Number = int(orderQuerySet.load_amount)
        Requirement.LoadWeight = float(orderQuerySet.load_weight)
        Requirement.TimeStart = str(orderQuerySet.start_time)
        Requirement.Inbound = int(orderQuerySet.start_point)
        Requirement.Outbound = int(orderQuerySet.end_point)
        Requirement.Date = str(orderQuerySet.order_date)
        order.append(Requirement)
        
        # Mark as not scheduled so it will be picked up by the scheduler
        orderQuerySet.is_scheduled = False
        orderQuerySet.save()
        
        logger.info(f"Rescheduling order #{orderNum}")
        BLL.schedule.Schedule.reschedule_agv(order)
        return True
        
    except Exception as e:
        logger.error(f"Error rescheduling order #{orderNum}: {e}")
        return False

def update_agv_positions():
    """
    Updates AGV positions using Position.returnPosition for accurate position calculation
    """
    try:
        logger.info("Updating AGV positions")
        
        now = datetime.datetime.now()
        date = now.date()
        now_timestamp = time.mktime(now.timetuple())
        
        # Get active (not completed) schedules
        active_schedules = schedule_data.objects.filter(
            order_date=date,
            is_processed=False
        )
        
        logger.info(f"Found {len(active_schedules)} active schedules to update positions")
        
        updated_count = 0
        for schedule in active_schedules:
            try:
                # Parse the instruction set
                instruction_set = json.loads(schedule.instruction_set)
                
                # Get the schedule times
                start_time = f"{schedule.order_date} {schedule.est_start_time}"
                end_time = f"{schedule.order_date} {schedule.est_end_time}"
                
                start_timestamp = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
                end_timestamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
                
                # Skip schedules that haven't started yet
                if start_timestamp > now_timestamp:
                    continue
                    
                # Check if the schedule has completed
                if end_timestamp < now_timestamp:
                    # Mark as processed/completed
                    schedule.is_processed = True
                    schedule.save()
                    logger.info(f"Marked schedule {schedule.schedule_id} as completed")
                    continue

                # Create a Schedule object for position calculation
                current_schedule = DTO.schedule.Schedule()
                current_schedule.TimeStart = schedule.est_start_time
                current_schedule.TimeEnd = schedule.est_end_time
                
                # Create Car object
                current_schedule.Car = DTO.agv_car.AGVCar()
                current_schedule.Car.CarId = instruction_set[0]
                
                # Convert instruction set to ListOfControlSignal
                current_schedule.ListOfControlSignal = []
                for i in range(1, len(instruction_set)-1):  # Skip first (ID) and last (endpoint)
                    control_signal = DTO.control_signal.ControlSignal()
                    control_signal.Road = DTO.road.Road(
                        instruction_set[i][0],  # FirstNode
                        instruction_set[i][1],  # SecondNode
                        instruction_set[i][3]   # Distance
                    )
                    control_signal.Velocity = instruction_set[i][2]  # Velocity
                    current_schedule.ListOfControlSignal.append(control_signal)
                
                # Calculate current position using Position.returnPosition
                current_time = now.strftime("%H:%M:%S")
                position = BLL.position.Position.returnPosition(current_time, current_schedule)
                
                # Create position data for MQTT
                position_data = {
                    "agv_id": str(current_schedule.Car.CarId),
                    "current_time": current_time,
                    "first_node": position.FirstNode,
                    "second_node": position.SecondNode,
                    "travelled_distance": position.TravelledDistance,
                    "is_active": True
                }
                
                # Publish position update
                topic = f"AGVPosition/{current_schedule.Car.CarId}"
                publishMsg(topic, json.dumps(position_data))
                updated_count += 1
                
            except Exception as schedule_error:
                logger.error(f"Error processing schedule {schedule.schedule_id}: {schedule_error}")
                continue

        if updated_count > 0:
            logger.info(f"Updated positions for {updated_count} active AGVs")
            
    except Exception as e:
        logger.error(f"Error updating AGV positions: {e}")

def start_position_update_thread(update_interval=5):
    """
    Starts a background thread that periodically updates AGV positions
    without regenerating schedules.
    
    Args:
        update_interval: Time in seconds between position updates (default: 5)
    """
    def position_update_worker():
        while True:
            try:
                update_agv_positions()
                time.sleep(update_interval)
            except Exception as e:
                logger.error(f"Error in position update thread: {e}")
                time.sleep(update_interval)
    
    position_thread = Thread(target=position_update_worker, daemon=True)
    position_thread.start()
    logger.info(f"Started position update thread (interval: {update_interval}s)")
    return position_thread