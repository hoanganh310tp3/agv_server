import DTO.schedule
import DTO.agv_car
import BLL.convert
import DTO.agv_car
import BLL.abc
import BLL.requirement
import BLL.car_selection
import BLL.schedule

class Schedule:
    @staticmethod
    def returnSchedule(Requirement, SelectedCarTrip, SelectedTransportingTrip):
        try:
            Schedule = DTO.schedule.Schedule()
            
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
            Schedule.ControlSignal = Schedule.list_control_signal()
            
            TimeStamp = BLL.convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
            TravelTime = BLL.convert.Convert.returnScheduleToTravellingTime(Schedule.ListOfControlSignal)
            Schedule.TimeEnd = BLL.convert.Convert.returnTimeStampToTime(TimeStamp + TravelTime + DTO.agv_car.AGVCar.delayTime)
            
            Schedule.TotalEnergy = round(SelectedCarTrip.Cost.CostValue + SelectedTransportingTrip.CostValue, 3)
            Schedule.TotalDistance = Schedule.get_total_distance()
            
            MaxBatteryCapacity = DTO.agv_car.AGVCar.MaxBatteryCapacity
            CurrentBattery = float(Schedule.Car.BatteryCapacity)
            EnergyUsed = float(Schedule.TotalEnergy)
            Schedule.Car.BatteryCapacity = round((CurrentBattery * MaxBatteryCapacity/100 - EnergyUsed) * 100/MaxBatteryCapacity, 2)
            Schedule.BatteryCapacity = Schedule.Car.BatteryCapacity
            
            Schedule.Car.ScheduleList.append(Schedule)
            
            return Schedule
        
        except Exception as e:
           print(f"Error creating schedule: {e}")
        return None

    @staticmethod
    def returnListOfSchedule():
        ListOfRequirement = BLL.requirement.Requirement.ReadTimeTable()
        NewABC = BLL.abc.ABC()
        BLL.car_selection.CarSelection.InitialCar()
        for EachRequirement in ListOfRequirement:
            NewABC = BLL.abc.ABC()
            SelectedCarTrip = BLL.car_selection.CarSelection.returnSelectedCar(EachRequirement)
            TimeStart = BLL.convert.Convert.TimeToTimeStamp(EachRequirement.TimeStart)
            if(len(SelectedCarTrip.Cost.ListOfControlSignal) > 1):
                TimeStart = BLL.convert.Convert.returnScheduleToTravellingTime(SelectedCarTrip.Cost.ListOfControlSignal) + TimeStart
            SelectedTransportingTrip = NewABC.ABCAlgorithm(NewABC,EachRequirement.Inbound,EachRequirement.Outbound,EachRequirement.LoadWeight,TimeStart)
            Schedule = BLL.schedule.Schedule.returnSchedule(EachRequirement,SelectedCarTrip,SelectedTransportingTrip)
            DTO.schedule.Schedule.ListOfSchedule.append(Schedule)

    @staticmethod
    def return_to_lot(startNode, stopNode, loadWeight, timeStart):
        NewABC = BLL.abc.ABC()
        Route=list()
        Route = NewABC.ABCAlgorithm(NewABC, startNode, stopNode, loadWeight, timeStart)
        return Route
