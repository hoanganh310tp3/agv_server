from . import road
from . import agv_car
from . import constrains
#Tạo và quản lý các tín hiệu điều khiển cho AGV.
class ControlSignal:
    
    def __init__(self, Road=""):
        self.Road = Road
        self.Velocity = agv_car.AGVCar.MaxVelocity
        self.Action = 1

    def __str__(self):
        return f"{self.Road.FirstNode} {self.Road.SecondNode} {self.Velocity} {self.Action}"

    @staticmethod
    def returnListOfControlSignal(TimeStart, ListOfNode):
        ListOfControlSignal = list()
        ListOfRoad = road.Road.returnListOfRoad(ListOfNode)
        for EachRoad in ListOfRoad:
            signal = constrains.Constrains.CollisionConstrain(TimeStart, EachRoad)
            ListOfControlSignal.append(signal)
        
        for Element in ListOfControlSignal:
            if Element.Velocity >= agv_car.AGVCar.MaxVelocity:
                Element.Velocity = agv_car.AGVCar.MaxVelocity
            elif Element.Velocity >= 0.20:
                Element.Velocity = 0.20
            elif Element.Velocity >= 0.15:
                Element.Velocity = 0.15
            elif Element.Velocity >= 0.1:
                Element.Velocity = 0.1
            else:
                Element.Velocity = 0.1
        return ListOfControlSignal

# 0 stop
# 1 go straight
# 2 turn right
# 3 turn left
# 4 reverse