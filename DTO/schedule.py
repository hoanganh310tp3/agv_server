import BLL.convert

class Schedule:
    ListOfSchedule = list()
    
    def __init__(self):
        self.ListOfControlSignal = list()
        self.Order = ""
        self.Date = ""
        self.Name = "Transporting"
        self.LoadAmount = 0
        self.LoadWeight = 0
        self.Car = ""
        self.BatteryCapacity = ""
        self.TotalEnergy = 0
        self.TotalDistance = 0
        self.TimeStart = ""
        self.TimeEnd = ""
        self.Inbound = ""
        self.Outbound = ""
        self.ControlSignal = ""
        
    def get_car_id(self):
        carID = ""
        carID = self.Car.CarId
        return carID

    def get_total_distance(self):
        TotalDistance = float(0)
        for EachControlSignal in self.ListOfControlSignal:
            TotalDistance = TotalDistance  + EachControlSignal.Road.Distance
        return TotalDistance
      
    def list_control_signal(self):
        ControlSignal = list()
        ControlSignal.append(self.get_car_id())
        for EachControlSignal in self.ListOfControlSignal:
            ControlSignal.append([EachControlSignal.Road.FirstNode, EachControlSignal.Road.SecondNode, EachControlSignal.Velocity, EachControlSignal.Road.Distance, EachControlSignal.Road.Direction])
         
        length = len(self.ListOfControlSignal)-1
        ControlSignal.append([self.ListOfControlSignal[length].Road.SecondNode, self.ListOfControlSignal[length].Road.SecondNode, 0, 0, 0])
        return ControlSignal

    