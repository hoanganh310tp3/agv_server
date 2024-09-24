import requirement
import abc
import schedule

from ManageRequests.models import DB_SimpleOrder

class Requirement:
    def __init__(self, Order="", Name="", Number="", Weight="", TimeStart="", Inbound="", Outbound="", CalledCar="", Date=""):
        self.Order = Order
        self.Name = Name
        self.CalledCar = CalledCar
        self.Date = Date
        self.LoadWeight = 0
        self.TimeStart = TimeStart
        self.Inbound = Inbound
        self.Outbound = Outbound
        self.Number = 0
    
    def __str__(self):
        return f"{self.Order}, {self.Date}, {self.Name}, {self.CalledCar}, {self.Inbound}, {self.Outbound}"

    @staticmethod
    def ReadTimeTable():
        orderQuerySet = DB_SimpleOrder.objects.all().order_by('start_time')
        
        listOfOrders = []
        
        for eachOrder in orderQuerySet:
            requirement = Requirement(
                Order=int(eachOrder.order_number),
                Date=str(eachOrder.order_date),
                Name=str(eachOrder.load_name),
                Number=int(eachOrder.load_amount),
                TimeStart=str(eachOrder.start_time),
                Inbound=int(eachOrder.from_node),
                Outbound=int(eachOrder.to_node)
            )
            requirement.LoadWeight = float(eachOrder.load_weight)
            listOfOrders.append(requirement)
            
        return listOfOrders

# Phương thức cũ đã bị comment out
# def ReadTimeTable():
#     ...