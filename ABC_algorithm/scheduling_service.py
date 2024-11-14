from ..requests_management.models import order_data, schedule_data
from ..agv_management.models import agv_identify
from . import schedule as abc_schedule
from django.db import transaction
import asyncio

async def process_pending_orders():
    while True:
        try:
            # Get unprocessed orders
            pending_orders = order_data.objects.filter(
                schedule_data__isnull=True
            ).order_by('start_time')

            if pending_orders.exists():
                # Process orders using ABC algorithm
                abc_schedule.Schedule.returnListOfSchedule()
                
                # Get the generated schedules
                for schedule_item in abc_schedule.Schedule.ListOfSchedule:
                    with transaction.atomic():
                        # Create new schedule_data entry
                        new_schedule = schedule_data(
                            order_number=order_data.objects.get(order_id=schedule_item.Order),
                            order_date=schedule_item.Date,
                            load_name=schedule_item.Name,
                            load_weight=schedule_item.LoadWeight,
                            load_amount=schedule_item.LoadAmount,
                            agv_id=schedule_item.get_car_id(),
                            est_energy=schedule_item.TotalEnergy,
                            est_distance=schedule_item.get_total_distance(),
                            est_start_time=schedule_item.TimeStart,
                            est_end_time=schedule_item.TimeEnd,
                            start_point=schedule_item.Inbound,
                            end_point=schedule_item.Outbound,
                            is_processed=True,
                            instruction_set=str(schedule_item.list_control_signal())
                        )
                        new_schedule.save()

        except Exception as e:
            print(f"Error processing orders: {str(e)}")
            
        # Wait for 30 seconds before checking again
        await asyncio.sleep(30) 