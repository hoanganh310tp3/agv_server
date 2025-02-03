import DTO.road
import BLL.road
import DTO.agv_car
import BLL.constrains
class ControlSignal:
    def returnListOfControlSignal(TimeStart, ListOfNode):
        ListOfControlSignal = list()
        ListOfRoad = BLL.road.Road.returnListOfRoad(ListOfNode)      
        for EachRoad in ListOfRoad:
            ListOfControlSignal.append(BLL.constrains.Constrains.CollisionConstrain(TimeStart,EachRoad))  
        for Element in ListOfControlSignal:
            if (Element.Velocity >= DTO.agv_car.AGVCar.MaxVelocity):
                Element.Velocity = DTO.agv_car.AGVCar.MaxVelocity
            elif (Element.Velocity >= 0.20):
                Element.Velocity = 0.20
            elif (Element.Velocity >= 0.15):
                Element.Velocity = 0.15
            elif (Element.Velocity >= 0.1):
                Element.Velocity = 0.1
            else:
                Element.Velocity = 0.1
        return ListOfControlSignal