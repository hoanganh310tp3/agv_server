from .map_execution import Map
from .abc import ABC
from .control_signal import ControlSignal
class Population:
    def __init__(self,Inbound = 0,Outbound = 0,LoadWeigth = 0,TimeStart = 0):
        if (int(Inbound) == 0 and  int(Outbound) == 0):
            self.TravelledNode = list()
            self.CostValue = float(100000)
            self.ListOfControlSignal = list()
            self.AbandonmentCounter = int(0)
            return
        self.TravelledNode = Bll.MapExecution.Map.returnFeasiblePath(Inbound,Outbound)
        if (len(self.TravelledNode) >= 1):
            if(self.TravelledNode[len(self.TravelledNode) - 1] == int(Outbound)):
                self.ListOfControlSignal = Bll.ControlSignal.ControlSignal.returnListOfControlSignal(TimeStart,self.TravelledNode)
                self.CostValue = Bll.ABC.ABC.returnCostFunction(self.ListOfControlSignal,Outbound,LoadWeigth)
                self.AbandonmentCounter = int(0)
                return
        self.CostValue = float(100000)
        self.ListOfControlSignal = list()
        self.AbandonmentCounter = int(0)