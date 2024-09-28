from . import abc
from . import schedule

from requests_management.models import order_data

class Requirement:
    def __init__(self, Order="", Name="", Number="", Weight="", TimeStart="", Inbound="", Outbound="", CalledCar="", Date=""):
        self.Order = Order
        self.Name = Name
        self.CalledCar = CalledCar
        self.Date = Date
        self.LoadWeight = Weight
        self.TimeStart = TimeStart
        self.Inbound = Inbound
        self.Outbound = Outbound
        self.Number = Number
    
    def __str__(self):
        return f"{self.Order}, {self.Date}, {self.Name}, {self.CalledCar}, {self.Inbound}, {self.Outbound}"

    @staticmethod
    def ReadTimeTable():
        orderQuerySet = order_data.objects.all().order_by('start_time')
        
        listOfOrders = list()
        
        for eachOrder in orderQuerySet:
            requirement = Requirement()
            requirement.Order = int(eachOrder.order_number)
            requirement.Date = str(eachOrder.order_date)
            requirement.Name = str(eachOrder.load_name)
            requirement.Number = int(eachOrder.load_amount)
            requirement.LoadWeight = float(eachOrder.load_weight)
            requirement.TimeStart = str(eachOrder.start_time)
            requirement.Inbound = int(eachOrder.from_node)
            requirement.Outbound = int(eachOrder.to_node)
            listOfOrders.append(requirement)
            
        return listOfOrders

    # def ReadTimeTable():
    #     f = open("TimeTable.csv",'r')
    #     temp = f.readline()
    #     ListOfRequirement = list()
    #     for line in f:
    #         temp = line.strip().split(',')
    #         requirement = Requirement()
    #         requirement.Order = int(temp[0])
    #         requirement.Name = str(temp[1])
    #         requirement.Number = int(temp[2])
    #         requirement.LoadWeight = float(temp[3])
    #         requirement.TimeStart = str(temp[4])
    #         requirement.Inbound = int(temp[5])
    #         requirement.Outbound = int(temp[6])
    #         ListOfRequirement.append(requirement)
    #     f.close()

    #     return ListOfRequirement