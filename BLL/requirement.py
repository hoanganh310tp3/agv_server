import DTO.requirement
import BLL.schedule
import DTO.schedule
import BLL.abc
import datetime
from requests_management.models import order_data

class Requirement:
    @staticmethod
    def ReadTimeTable():
        try:
            orderQuerySet = order_data.objects.all().order_by('start_time')
            
            if not orderQuerySet.exists():
                print("No orders found")
                return []
                
            listOfOrders = []
            
            for eachOrder in orderQuerySet:
                try:
                    requirement = DTO.requirement.Requirement()
                    requirement.Order = int(eachOrder.order_number)
                    requirement.Date = str(eachOrder.order_date)
                    requirement.Name = str(eachOrder.load_name)
                    requirement.Number = int(eachOrder.load_amount)
                    requirement.LoadWeight = float(eachOrder.load_weight)
                    requirement.TimeStart = str(eachOrder.start_time)
                    requirement.Inbound = int(eachOrder.start_point)
                    requirement.Outbound = int(eachOrder.end_point)
                    listOfOrders.append(requirement)
                    
                except Exception as e:
                    print(f"Error processing order {eachOrder.order_id}: {e}")
                    continue
                    
            return listOfOrders
            
        except Exception as e:
            print(f"Error reading time table: {e}")
            return []