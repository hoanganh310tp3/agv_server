import schedule
import road
import position
import control_signal
import convert
#Xác định vị trí của AGV dựa trên thời gian và lịch trình.
class Position:
    def __init__(self):
        self.FirstNode = ""
        self.SecondNode = ""
        self.TravelledDistance = ""
        self.Car = ""
        self.Velocity = ""

    @staticmethod 
    def returnPosition(Time, Schedule):
        position_instance = Position()  # Sử dụng tên biến khác để tránh nhầm lẫn
        TimeCounter = convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
        Index = 0
        TimeEnd = convert.Convert.TimeToTimeStamp(Schedule.TimeEnd)
        while TimeCounter <= TimeEnd:
            Distance = Schedule.ListOfControlSignal[Index].Road.Distance
            Velocity = Schedule.ListOfControlSignal[Index].Velocity
            if TimeCounter + Distance / Velocity > Time:
                position_instance.FirstNode = Schedule.ListOfControlSignal[Index].Road.FirstNode
                position_instance.SecondNode = Schedule.ListOfControlSignal[Index].Road.SecondNode
                position_instance.TravelledDistance = float(Velocity) * (Time - TimeCounter)
                position_instance.Car = Schedule.Car
                position_instance.Velocity = Velocity  # Sửa lỗi gán giá trị
                return position_instance
            Index += 1
            if Index == len(Schedule.ListOfControlSignal):
                break
            TimeCounter += Distance / Velocity 
        return position_instance
