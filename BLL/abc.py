
import BLL.cost_function
import DTO.population
import DTO.abc_parameter
import numpy
import BLL.map_execution


class ABC:
    def __init__(self):
        self.BestCost = DTO.population.Population() 
        self.ListOfPop = list()
        self.ListOfFitnessValue = [0]*DTO.abc_parameter.ABCSetting.nPop
        self.ListOfProbability = [0]*DTO.abc_parameter.ABCSetting.nPop
        self.BestCostList = list()
        
    @staticmethod
    def returnCostFunction(ListOfControlSignal,Outbound,LoadWeight):
        CostFunctionValue = float(0)
        
        if(int(ListOfControlSignal[len(ListOfControlSignal)-int(1)].Road.SecondNode) != int(Outbound)):
            return float(100000)
        else:    
            CostFunctionValue = BLL.cost_function.CostFunction.returnCostFunction(ListOfControlSignal,LoadWeight)
        return CostFunctionValue
    
    @staticmethod
    def CreateInitialPopulation(self,Inbound,Outbound,LoadWeigth,TimeStart):
        NumberOfPopulation = DTO.abc_parameter.ABCSetting.nPop 
        for i in range (NumberOfPopulation):
            NewPop = DTO.population.Population(Inbound,Outbound,LoadWeigth,TimeStart)
            if(self.BestCost.CostValue >= NewPop.CostValue):
                self.BestCostList.append(self.BestCost.CostValue)
                self.BestCost = NewPop
            self.ListOfPop.append(NewPop)
    
    @staticmethod
    def RecruitedBees(self):
        NumberOfPopulation = DTO.abc_parameter.ABCSetting.nPop 
        
        for i in range (NumberOfPopulation):
            NewBee = DTO.population.Population()                
            if (NewBee.CostValue <= self.ListOfPop[i].CostValue):
                self.ListOfPop[i].CostValue = NewBee.CostValue
            else:
                self.ListOfPop[i].AbandonmentCounter = self.ListOfPop[i].AbandonmentCounter + 1
    
    @staticmethod
    def CalculateFitness(self):
        SumOfFitness = float(0)
        NumberOfPopulation = DTO.abc_parameter.ABCSetting.nPop
        for i in range(NumberOfPopulation):
            FitnessValue = 1/float(1+self.ListOfPop[i].CostValue)
            self.ListOfFitnessValue[i] = FitnessValue 
            SumOfFitness = SumOfFitness + FitnessValue
        
        for i in range(NumberOfPopulation):
            self.ListOfProbability[i] = self.ListOfFitnessValue[i]/SumOfFitness
       
    @staticmethod    
    def RouletteWheelSelection(self):
        RandomNumber = numpy.random.uniform(0,1)
        Probability = self.ListOfProbability[0]
        for i in range (len(self.ListOfProbability)):
            if(RandomNumber < Probability):
                return int(i)
            else:
                Probability = Probability + self.ListOfProbability[i]
                
    @staticmethod
    def OnlookerBees(self):
        NumberOfOnlooker = DTO.abc_parameter.ABCSetting.nOnlooker
        for i  in range (NumberOfOnlooker):
            Source = self.RouletteWheelSelection(self)
            NewBee = DTO.population.Population() 
            
            if (NewBee.CostValue <= self.ListOfPop[i].CostValue):
                self.ListOfPop[i] = NewBee
            else:
                self.ListOfPop[i].AbandonmentCounter = self.ListOfPop[i].AbandonmentCounter + 1
    
    @staticmethod
    def ScoutBees(self):
        NumberOfPopulation = DTO.abc_parameter.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].AbandonmentCounter >= DTO.abc_parameter.ABCSetting.L):
                self.ListOfPop[i] = DTO.population.Population()
                self.ListOfPop[i].AbandonmentCounter = 0
    
    @staticmethod
    def BestSolution(self):
        NumberOfPopulation = DTO.abc_parameter.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].CostValue <= self.BestCost.CostValue):
                self.BestCost = self.ListOfPop[i]
                self.BestCostList.append(self.BestCost.CostValue)
    
    @staticmethod
    def ABCAlgorithm(self,Inbound,Outbound,LoadWeight,TimeStart):

        for i in range(DTO.abc_parameter.ABCSetting.MaxIt):
            self.CreateInitialPopulation(self,Inbound,Outbound,LoadWeight,TimeStart)
            self.RecruitedBees(self)
            self.CalculateFitness(self)
            self.OnlookerBees(self)
            self.ScoutBees(self)
            self.BestSolution(self)
        return self.BestCost
