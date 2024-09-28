from . import schedule
from . import road
from . import convert

class Position:
    def __init__(self):
        self.FirstNode = ""
        self.SecondNode = ""
        self.TravelledDistance = ""
        self.Car = ""
        self.Velocity = ""

    @staticmethod 
    def returnPosition(Time, Schedule):
        position = Position()
        TimeCounter = convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
        Index = 0
        TimeEnd = convert.Convert.TimeToTimeStamp(Schedule.TimeEnd)
        while TimeCounter <= TimeEnd:
            Distance = Schedule.ListOfControlSignal[Index].Road.Distance
            Velocity = Schedule.ListOfControlSignal[Index].Velocity
            if TimeCounter + Distance / Velocity > Time:
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