import BLL.requirement
import DTO.agv_car
import BLL.abc
import DTO.schedule
import DTO.population
import DTO.selected_car_trip
import BLL.convert
import DTO.requirement

from agv_management.active_agv import list_active_AGV

class CarSelection:
    @staticmethod
    def InitialCar():
        try:
            aAGV = []
            DTO.agv_car.AGVCar.CarList = []
            aAGV = list_active_AGV()
            
            print(f"Active AGVs found: {aAGV}")  # Add this debug line
            
            if not aAGV:
                print("No active AGVs found")
                return False

            for eachCar in aAGV:
                NewCar = DTO.agv_car.AGVCar()
                NewCar.CarId = eachCar[0]
                NewCar.Location = eachCar[1] 
                print(f"Initializing car: ID={eachCar[0]}, Location={eachCar[1]}")  # Add this debug line
                DTO.agv_car.AGVCar.CarList.append(NewCar)
            
            print(f"Total cars initialized: {len(DTO.agv_car.AGVCar.CarList)}")  # Add this debug line
            return True
                
        except Exception as e:
            print(f"Error initializing cars: {e}")
            return False

    
    @staticmethod
    def returnSelectedCar(Requirement):
        Weight = float(0)
        ListOfCar = [1]*(len(DTO.agv_car.AGVCar.CarList) + 1)
        TempList = [None]*(len(DTO.agv_car.AGVCar.CarList) + 1)
    
        for i in range(len(ListOfCar)):
            TempList[i] = Requirement.TimeStart
        
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = BLL.convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - BLL.convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
            else: 
                TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = BLL.convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - BLL.convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
                else: 
                    TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
        NewABC = BLL.abc.ABC()
        BestCar = DTO.selected_car_trip.SelectedCarTrip("",DTO.population.Population())
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(ListOfCar[int(EachCar.CarId)] == 1):
                TimeStart = BLL.convert.Convert.TimeToTimeStamp(TempList[EachCar.CarId])
                TempBestCost = DTO.population.Population()
                if(int(EachCar.Location) == int(Requirement.Inbound)):
                    TempBestCost.CostValue = 0
                else:
                    TempBestCost = NewABC.ABCAlgorithm(NewABC,int(EachCar.Location),int(Requirement.Inbound),Weight,TimeStart)
                if(TempBestCost.CostValue < BestCar.Cost.CostValue):
                    BestCar.Cost = TempBestCost
                    BestCar.Car = EachCar
        Requirement.TimeStart = TempList[int(BestCar.Car.CarId)]
        return BestCar
        