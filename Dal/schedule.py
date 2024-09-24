import ABC_algorithm.schedule
class Schedule:
    @staticmethod
    def SaveSchedule():
        f = open('Schedule.csv','w') 
        f.write("Order,Name,CarId,BatteryCapacity,TotalEnergy,WeightLoad,TimeStart,TimeEnd,Inbound,Outbound,TotalDistance")
        f.write("\n")
        for EachSchedule in ABC_algorithm.schedule.Schedule.ListOfSchedule:
            TotalDistance = float(0)
            f.write(str(EachSchedule.Order))
            f.write(",")
            f.write(str(EachSchedule.Name))
            f.write(",")
            f.write(str(EachSchedule.Car.CarId))
            f.write(",")
            f.write(str(EachSchedule.BatteryCapacity))
            f.write(",")
            f.write(str(EachSchedule.TotalEnergy))
            f.write(",")
            f.write(str(EachSchedule.LoadWeight))
            f.write(",")
            f.write(str(EachSchedule.TimeStart))
            f.write(",")
            f.write(str(EachSchedule.TimeEnd))
            f.write(",")
            f.write(str(EachSchedule.Inbound))
            f.write(",")
            f.write(str(EachSchedule.Outbound))
            f.write(",")
            for EachControlSignal in EachSchedule.ListOfControlSignal:
                TotalDistance = TotalDistance + EachControlSignal.Road.Distance
            f.write(str(TotalDistance))
            f.write(",")
            for EachControlSignal in EachSchedule.ListOfControlSignal:
                f.write(str(EachControlSignal.Road.FirstNode))
                f.write(str(EachControlSignal.Road.SecondNode))
                f.write("("+ str(EachControlSignal.Road.Distance) +" m)")
                f.write("("+ str(EachControlSignal.Velocity) +" m/s)")
                f.write(",")
            f.write("\n")  
        f.close()
        
#Lưu trữ và quản lý lịch trình của AGV.