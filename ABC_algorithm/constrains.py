import schedule
import position
import agv_car
import control_signal
import road
import convert
#Áp dụng các ràng buộc để đảm bảo an toàn và hiệu quả cho AGV
class Constrains:
    def CollisionConstrain(TimeStart,Road):
        Test = convert.Convert.returnTimeStampToTime(TimeStart)
        
        ControlSignal = control_signal.ControlSignal(Road)
        if(len(schedule.Schedule.ListOfSchedule) > 0):
            for EachSchedule in schedule.Schedule.ListOfSchedule:
                returnPosition = position.Position.returnPosition(TimeStart,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal
                    # Node constrain  
                    # Similar direction
                    ControlSignal.Road = Road
                    if(Road.FirstNode == returnPosition.FirstNode and returnPosition.TravelledDistance < agv_car.AGVCar.SafetyDistance):
                        ControlSignal.Velocity = float(returnPosition.TravelledDistance)/(float(agv_car.AGVCar.SafetyDistance)*agv_car.AGVCar.MaxVelocity)
                        continue

                TimeEnd = TimeStart + Road.Distance/ControlSignal.Velocity
                # Middle point
                returnPosition = position.Position.returnPosition(TimeStart + (TimeEnd - TimeStart)/2,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal

                # End point
                returnPosition = position.Position.returnPosition(TimeEnd-0.1,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal
                # Node constrain  
                # Similar direction
                ControlSignal.Road = Road
                if(Road.SecondNode == returnPosition.SecondNode and  Road.Distance - returnPosition.TravelledDistance  < agv_car.AGVCar.SafetyDistance):
                    ControlSignal.Velocity = round(Road.Distance/(float(Road.Distance - returnPosition.TravelledDistance + agv_car.AGVCar.SafetyDistance)/agv_car.AGVCar.MaxVelocity + float(Road.Distance)/agv_car.AGVCar.MaxVelocity),2)
                    continue
                # Different direction
                if(Road.SecondNode == returnPosition.FirstNode and (returnPosition.TravelledDistance < agv_car.AGVCar.SafetyDistance)):
                    ControlSignal.Velocity  = ControlSignal.Road.Distance*ControlSignal.Velocity/(agv_car.AGVCar.SafetyDistance - returnPosition.TravelledDistance + ControlSignal.Road.Distance)
                    continue

        return ControlSignal