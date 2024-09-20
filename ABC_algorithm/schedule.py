import convert
import abc
import car_selection

import requirement
import agv_car
import schedule



from agv_car import AGVCar

class Schedule:
    ListOfSchedule = []
    
    def __init__(self):
        self.ListOfControlSignal = []
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

    @staticmethod
    def returnSchedule(Requirement, SelectedCarTrip, SelectedTransportingTrip):
        Schedule = Schedule()
        Schedule.Name = Requirement.Name
        Schedule.Order = Requirement.Order
        Schedule.Date = Requirement.Date
        Schedule.Car = SelectedCarTrip.Car
        Schedule.Car.Location = Requirement.Outbound
        Schedule.Inbound = Requirement.Inbound
        Schedule.Outbound = Requirement.Outbound
        Schedule.TimeStart = Requirement.TimeStart
        Schedule.LoadWeight = Requirement.LoadWeight
        Schedule.ListOfControlSignal = SelectedCarTrip.Cost.ListOfControlSignal + SelectedTransportingTrip.ListOfControlSignal
        Schedule.TimeEnd = convert.Convert.returnTimeStampToTime(convert.Convert.TimeToTimeStamp(Schedule.TimeStart) + convert.Convert.returnScheduleToTravellingTime(Schedule.ListOfControlSignal) + AGVCar.delayTime)
        Schedule.TotalEnergy = round(SelectedCarTrip.Cost.CostValue + SelectedTransportingTrip.CostValue, 3)
        Schedule.Car.BatteryCapacity = round((float(Schedule.Car.BatteryCapacity) * AGVCar.MaxBatteryCapacity / 100 - float(Schedule.TotalEnergy)) * float(100) / (AGVCar.MaxBatteryCapacity), 2)
        Schedule.BatteryCapacity = Schedule.Car.BatteryCapacity
        Schedule.Car.ScheduleList.append(Schedule)
        return Schedule

    @staticmethod
    def returnListOfSchedule():
        ListOfRequirement = Requirement.ReadTimeTable()
        NewABC = ABC()
        CarSelection.InitialCar()
        for EachRequirement in ListOfRequirement:
            NewABC = ABC()
            SelectedCarTrip = CarSelection.returnSelectedCar(EachRequirement)
            TimeStart = convert.Convert.TimeToTimeStamp(EachRequirement.TimeStart)
            if len(SelectedCarTrip.Cost.ListOfControlSignal) > 1:
                TimeStart = convert.Convert.returnScheduleToTravellingTime(SelectedCarTrip.Cost.ListOfControlSignal) + TimeStart
            SelectedTransportingTrip = NewABC.ABCAlgorithm(NewABC, EachRequirement.Inbound, EachRequirement.Outbound, EachRequirement.LoadWeight, TimeStart)
            Schedule = Schedule.returnSchedule(EachRequirement, SelectedCarTrip, SelectedTransportingTrip)
            Schedule.ListOfSchedule.append(Schedule)

    @staticmethod
    def return_to_lot(startNode, stopNode, loadWeight, timeStart):
        NewABC = ABC()
        Route = NewABC.ABCAlgorithm(NewABC, startNode, stopNode, loadWeight, timeStart)
        return Route

    def get_car_id(self):
        return self.Car.CarId

    def get_total_distance(self):
        TotalDistance = 0.0
        for EachControlSignal in self.ListOfControlSignal:
            TotalDistance += EachControlSignal.Road.Distance
        return TotalDistance

    def list_control_signal(self):
        ControlSignal = [self.get_car_id()]
        for EachControlSignal in self.ListOfControlSignal:
            ControlSignal.append([EachControlSignal.Road.FirstNode, EachControlSignal.Road.SecondNode, EachControlSignal.Velocity, EachControlSignal.Road.Distance, EachControlSignal.Road.Direction])
        
        length = len(self.ListOfControlSignal) - 1
        ControlSignal.append([self.ListOfControlSignal[length].Road.SecondNode, self.ListOfControlSignal[length].Road.SecondNode, 0, 0, 0])
        return ControlSignal