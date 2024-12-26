import DTO.schedule
import DTO.road
import DTO.position
import DTO.control_signal
import BLL.convert

class Position:
    @staticmethod 
    def returnPosition(Time, Schedule):
        position = DTO.position.Position()
        TimeCounter = BLL.convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
        Index = 0
        TimeEnd = BLL.convert.Convert.TimeToTimeStamp(Schedule.TimeEnd)
        while (TimeCounter <= TimeEnd):
            Distance = Schedule.ListOfControlSignal[Index].Road.Distance
            Velocity = Schedule.ListOfControlSignal[Index].Velocity
            if (TimeCounter + Distance / Velocity > Time):
                position.FirstNode = Schedule.ListOfControlSignal[Index].Road.FirstNode
                position.SecondNode = Schedule.ListOfControlSignal[Index].Road.SecondNode
                position.TravelledDistance = float(Velocity) * (Time - TimeCounter)
                position.Car = Schedule.Car
                position.Velocity = Schedule.Car
                return position
            Index += 1
            if Index == len(Schedule.ListOfControlSignal):
                break
            TimeCounter += Distance / Velocity 
        return position