import DTO.schedule
import DTO.agv_car
import BLL.convert
import DTO.agv_car
import BLL.abc
import BLL.requirement
import BLL.car_selection
import BLL.schedule
#Đoạn code này định nghĩa lớp Schedule để quản lý lịch trình vận chuyển của các xe AGV, bao gồm việc tính toán và tạo ra lịch trình cho các yêu cầu vận chuyển.
class Schedule:
    @staticmethod
    def returnSchedule(Requirement, SelectedCarTrip, SelectedTransportingTrip):
        try:
        # Create new Schedule object
            Schedule = DTO.schedule.Schedule()
        
        # Set basic properties
            Schedule.Name = Requirement.Name
            Schedule.Order = Requirement.Order
            Schedule.Date = Requirement.Date
            Schedule.Car = SelectedCarTrip.Car
            Schedule.Car.Location = Requirement.Outbound
            Schedule.Inbound = Requirement.Inbound
            Schedule.Outbound = Requirement.Outbound
            Schedule.TimeStart = Requirement.TimeStart
            Schedule.LoadWeight = Requirement.LoadWeight
        
        # Combine control signals and convert to proper format
            Schedule.ListOfControlSignal = SelectedCarTrip.Cost.ListOfControlSignal + SelectedTransportingTrip.ListOfControlSignal
            Schedule.ControlSignal = Schedule.list_control_signal()  # Convert to database-friendly format
        
        # Calculate end time and energy
            TimeStamp = BLL.convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
            TravelTime = BLL.convert.Convert.returnScheduleToTravellingTime(Schedule.ListOfControlSignal)
            Schedule.TimeEnd = BLL.convert.Convert.returnTimeStampToTime(TimeStamp + TravelTime + DTO.agv_car.AGVCar.delayTime)
        
        # Calculate energy consumption
            Schedule.TotalEnergy = round(SelectedCarTrip.Cost.CostValue + SelectedTransportingTrip.CostValue, 3)
            Schedule.TotalDistance = Schedule.get_total_distance()
        
        # Update battery capacity
            MaxBatteryCapacity = DTO.agv_car.AGVCar.MaxBatteryCapacity
            CurrentBattery = float(Schedule.Car.BatteryCapacity)
            EnergyUsed = float(Schedule.TotalEnergy)
            Schedule.Car.BatteryCapacity = round((CurrentBattery * MaxBatteryCapacity/100 - EnergyUsed) * 100/MaxBatteryCapacity, 2)
            Schedule.BatteryCapacity = Schedule.Car.BatteryCapacity
        
        # Add to car's schedule list
            Schedule.Car.ScheduleList.append(Schedule)
        
            return Schedule
        
        except Exception as e:
           print(f"Error creating schedule: {e}")
        return None
    
    @staticmethod
    def returnListOfSchedule():
        try:
            # Clear old schedules
            DTO.schedule.Schedule.ListOfSchedule = []
            
            # Get requirements
            ListOfRequirement = BLL.requirement.Requirement.ReadTimeTable()
            if not ListOfRequirement:
                print("No requirements found")
                return False
                
            # Initialize cars
            if not BLL.car_selection.CarSelection.InitialCar():
                print("Failed to initialize cars")
                return False
                
            # Process each requirement
            for EachRequirement in ListOfRequirement:
                try:
                    NewABC = BLL.abc.ABC()
                    SelectedCarTrip = BLL.car_selection.CarSelection.returnSelectedCar(EachRequirement)
                    
                    if not SelectedCarTrip or not SelectedCarTrip.Car:
                        print(f"No suitable car for requirement {EachRequirement.Order}")
                        continue
                        
                    TimeStart = BLL.convert.Convert.TimeToTimeStamp(EachRequirement.TimeStart)
                    
                    if SelectedCarTrip.Cost and SelectedCarTrip.Cost.ListOfControlSignal and len(SelectedCarTrip.Cost.ListOfControlSignal) > 1:
                        TimeStart += BLL.convert.Convert.returnScheduleToTravellingTime(SelectedCarTrip.Cost.ListOfControlSignal)
                        
                    SelectedTransportingTrip = NewABC.ABCAlgorithm(NewABC, EachRequirement.Inbound, 
                                                               EachRequirement.Outbound,
                                                               EachRequirement.LoadWeight, 
                                                               TimeStart)
                    
                    if SelectedTransportingTrip:
                        Schedule = BLL.schedule.Schedule.returnSchedule(EachRequirement, 
                                                                   SelectedCarTrip,
                                                                   SelectedTransportingTrip)
                        if Schedule:
                            DTO.schedule.Schedule.ListOfSchedule.append(Schedule)
                        
                except Exception as e:
                    print(f"Error processing requirement {EachRequirement.Order}: {e}")
                    continue
                    
            return len(DTO.schedule.Schedule.ListOfSchedule) > 0
            
        except Exception as e:
            print(f"Error in returnListOfSchedule: {e}")
            return False

    @staticmethod
    def return_to_lot(startNode, stopNode, loadWeight, timeStart):
        # Tạo một đối tượng ABC mới
        NewABC = BLL.abc.ABC()
        Route=list()
        # Tạo lộ trình quay lại bãi bằng thuật toán ABC
        Route = NewABC.ABCAlgorithm(NewABC, startNode, stopNode, loadWeight, timeStart)
        return Route
