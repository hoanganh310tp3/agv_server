import DTO.schedule
import DTO.road
import BLL.position
import DTO.agv_car
import DTO.control_signal
import BLL.road
import BLL.convert

class Constrains:
    def CollisionConstrain(TimeStart,Road):
        Test = BLL.convert.Convert.returnTimeStampToTime(TimeStart)
        
        ControlSignal = DTO.control_signal.ControlSignal(Road)

        if(len(DTO.schedule.Schedule.ListOfSchedule) > 0):
            for EachSchedule in DTO.schedule.Schedule.ListOfSchedule:
                returnPosition = BLL.position.Position.returnPosition(TimeStart,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = DTO.road.Road(0,0,100000)
                        ControlSignal.Velocity = DTO.agv_car.AGVCar.MaxVelocity
                        return ControlSignal

                    ControlSignal.Road = Road
                    if(Road.FirstNode == returnPosition.FirstNode and returnPosition.TravelledDistance < DTO.agv_car.AGVCar.SafetyDistance):
                        ControlSignal.Velocity = float(returnPosition.TravelledDistance)/(float(DTO.agv_car.AGVCar.SafetyDistance)*DTO.agv_car.AGVCar.MaxVelocity)
                        continue

                TimeEnd = TimeStart + Road.Distance/ControlSignal.Velocity
                
                returnPosition = BLL.position.Position.returnPosition(TimeStart + (TimeEnd - TimeStart)/2,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = DTO.road.Road(0,0,100000)
                        ControlSignal.Velocity = DTO.agv_car.AGVCar.MaxVelocity
                        return ControlSignal

                returnPosition = BLL.position.Position.returnPosition(TimeEnd-0.1,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = DTO.road.Road(0,0,100000)
                        ControlSignal.Velocity = DTO.agv_car.AGVCar.MaxVelocity
                        return ControlSignal
                
                ControlSignal.Road = Road
                if(Road.SecondNode == returnPosition.SecondNode and  Road.Distance - returnPosition.TravelledDistance  < DTO.agv_car.AGVCar.SafetyDistance):
                    ControlSignal.Velocity = round(Road.Distance/(float(Road.Distance - returnPosition.TravelledDistance + DTO.agv_car.AGVCar.SafetyDistance)/DTO.agv_car.AGVCar.MaxVelocity + float(Road.Distance)/DTO.agv_car.AGVCar.MaxVelocity),2)
                    continue

                if(Road.SecondNode == returnPosition.FirstNode and (returnPosition.TravelledDistance < DTO.agv_car.AGVCar.SafetyDistance)): 
                    ControlSignal.Velocity  = ControlSignal.Road.Distance*ControlSignal.Velocity/(DTO.agv_car.AGVCar.SafetyDistance - returnPosition.TravelledDistance + ControlSignal.Road.Distance)
                    continue

        return ControlSignal