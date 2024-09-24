
import agv_car
import abc
import population
import selected_car_trip
import convert

from requirement import Requirement
from agv_management.active_agv import list_active_AGV

#Lựa chọn xe AGV dựa trên các yêu cầu và điều kiện.

class CarSelection:
    @staticmethod
    def InitialCar():
        aAGV = list()
        agv_car.AGVCar.CarList = []
        aAGV = list_active_AGV()

        for eachCar in aAGV:
            NewCar = agv_car.AGVCar()
            NewCar.CarId = eachCar[0]
            NewCar.Location = eachCar[1]
            print(eachCar)
            agv_car.AGVCar.CarList.append(NewCar)

    @staticmethod
    def returnSelectedCar(Requirement):
        Weight = float(0)
        ListOfCar = [1]*len(agv_car.AGVCar.CarList)
        TempList = [None]*len(agv_car.AGVCar.CarList)
        
        for i in range(len(ListOfCar)):
            TempList[i] = Requirement.TimeStart

        for EachCar in agv_car.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
                else: 
                    TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
   
        NewABC = abc.ABC()
        BestCar = selected_car_trip.SelectedCarTrip("",population.Population())
        for EachCar in agv_car.AGVCar.CarList:
            if(ListOfCar[int(EachCar.CarId)] == 1):
                TimeStart = convert.Convert.TimeToTimeStamp(TempList[EachCar.CarId])
                TempBestCost = population.Population()
                if(int(EachCar.Location) == int(Requirement.Inbound)):
                    TempBestCost.CostValue = 0
                else:
                    TempBestCost = NewABC.ABCAlgorithm(NewABC,int(EachCar.Location),int(Requirement.Inbound),Weight,TimeStart)
                if(TempBestCost.CostValue < BestCar.Cost.CostValue):
                    BestCar.Cost = TempBestCost
                    BestCar.Car = EachCar

        Requirement.TimeStart = TempList[int(BestCar.Car.CarId)]
        return BestCar
        