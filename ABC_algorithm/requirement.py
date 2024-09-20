
import abc
import schedule


from ManageRequests.models import DB_SimpleOrder

#below class is from dto_requirement.py of code_anh_minh. And in this file i mix 2 requirement.py 
class Dto_Requirement:
    def __init__(self,Order="",Name="",Number = "",Weight="",TimeStart="",Inbound="",Outbound="", CalledCar ="", Date =""):
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

class Requirement:
    @staticmethod

    def ReadTimeTable():
        orderQuerySet = DB_SimpleOrder.objects.all().order_by('start_time')
        
        listOfOrders = list()
        
        for eachOrder in orderQuerySet:
            Requirement = Dto_Requirement.Requirement()
            Requirement.Order = int(eachOrder.order_number)
            Requirement.Date = str(eachOrder.order_date)
            Requirement.Name = str(eachOrder.load_name)
            Requirement.Number = int(eachOrder.load_amount)
            Requirement.LoadWeight = float(eachOrder.load_weight)
            Requirement.TimeStart = str(eachOrder.start_time)
            Requirement.Inbound = int(eachOrder.from_node)
            Requirement.Outbound = int(eachOrder.to_node)
            listOfOrders.append(Requirement)
            
        return listOfOrders

    # def ReadTimeTable():
    #     f = open("TimeTable.csv",'r')
    #     temp = f.readline()
    #     ListOfRequirement = list()
    #     for line in f:
    #         temp = line.strip().split(',')
    #         Requirement = Dto.Requirement.Requirement()
    #         Requirement.Order = int(temp[0])
    #         Requirement.Name = str(temp[1])
    #         Requirement.Number = int(temp[2])
    #         Requirement.LoadWeight = float(temp[3])
    #         Requirement.TimeStart = str(temp[4])
    #         Requirement.Inbound = int(temp[5])
    #         Requirement.Outbound = int(temp[6])
    #         ListOfRequirement.append(Requirement)
    #     f.close()

    #     return ListOfRequirement
   