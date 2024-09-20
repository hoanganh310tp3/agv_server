import requirement
import agv_car
import abc
import schedule

import population
import selected_car_trip
import convert


from ManageAGV.activeAGV import list_active_AGV



class CarSelection:
    @staticmethod
    def InitialCar():
        aAGV = list()
        Dto.AGVCar.AGVCar.CarList = []
        aAGV = list_active_AGV()

        for eachCar in aAGV:
            NewCar = Dto.AGVCar.AGVCar()
            NewCar.CarId = eachCar[0]
            NewCar.Location = eachCar[1]
            print(eachCar)
            Dto.AGVCar.AGVCar.CarList.append(NewCar)

    @staticmethod
    def returnSelectedCar(Requirement):
        Weight = float(0)
        ListOfCar = [1]*len(Dto.AGVCar.AGVCar.CarList)
        TempList = [None]*len(Dto.AGVCar.AGVCar.CarList)
        
        for i in range(len(ListOfCar)):
            TempList[i] = Requirement.TimeStart

        for EachCar in Dto.AGVCar.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = Bll.Convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - Bll.Convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
                else: 
                    TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
   
        NewABC = Bll.ABC.ABC()
        BestCar = Dto.SelectedCarTrip.SelectedCarTrip("",Dto.Population.Population())
        for EachCar in Dto.AGVCar.AGVCar.CarList:
            if(ListOfCar[int(EachCar.CarId)] == 1):
                TimeStart = Bll.Convert.Convert.TimeToTimeStamp(TempList[EachCar.CarId])
                TempBestCost = Dto.Population.Population()
                if(int(EachCar.Location) == int(Requirement.Inbound)):
                    TempBestCost.CostValue = 0
                else:
                    TempBestCost = NewABC.ABCAlgorithm(NewABC,int(EachCar.Location),int(Requirement.Inbound),Weight,TimeStart)
                if(TempBestCost.CostValue < BestCar.Cost.CostValue):
                    BestCar.Cost = TempBestCost
                    BestCar.Car = EachCar

        Requirement.TimeStart = TempList[int(BestCar.Car.CarId)]
        return BestCar
        