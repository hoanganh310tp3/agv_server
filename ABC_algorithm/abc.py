import numpy
from . import population
from . import abc_parameters
from . import cost_function
#Định nghĩa và triển khai thuật toán ABC (Artificial Bee Colony).
class ABC:
    def __init__(self):
        self.BestCost = population.Population()
        self.ListOfPop = list()
        self.ListOfFitnessValue = [0]*abc_parameters.ABCSetting.nPop
        self.ListOfProbability = [0]*abc_parameters.ABCSetting.nPop
        self.BestCostList = list()
        
    @staticmethod
    def returnCostFunction(ListOfControlSignal,Outbound,LoadWeight):
        CostFunctionValue = float(0)
        
        if(int(ListOfControlSignal[len(ListOfControlSignal)-int(1)].Road.SecondNode) != int(Outbound)):
            return float(100000)
        else:    
            CostFunctionValue = cost_function.CostFunction.returnCostFunction(ListOfControlSignal,LoadWeight)
        return CostFunctionValue
    
    @staticmethod
    def CreateInitialPopulation(self,Inbound,Outbound,LoadWeigth,TimeStart):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop 
        for i in range (NumberOfPopulation):
            NewPop = population.Population(Inbound,Outbound,LoadWeigth,TimeStart)
            if(self.BestCost.CostValue >= NewPop.CostValue):
                self.BestCostList.append(self.BestCost.CostValue)
                self.BestCost = NewPop
            self.ListOfPop.append(NewPop)
            
    @staticmethod
    def RecruitedBees(self):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop 
        
        for i in range (NumberOfPopulation):
            # New Bee Generation
            NewBee = population.Population()                
            # Comparision
            if (NewBee.CostValue <= self.ListOfPop[i].CostValue):
                self.ListOfPop[i].CostValue = NewBee.CostValue
            else:
                self.ListOfPop[i].AbandonmentCounter = self.ListOfPop[i].AbandonmentCounter + 1
    
    @staticmethod
    # Calculate Fitness Value
    def CalculateFitness(self):
        SumOfFitness = float(0)
        NumberOfPopulation = abc_parameters.ABCSetting.nPop
        for i in range(NumberOfPopulation):
            # Calculate fitness value
            FitnessValue = 1/float(1+self.ListOfPop[i].CostValue)
            self.ListOfFitnessValue[i] = FitnessValue 
            SumOfFitness = SumOfFitness + FitnessValue
        
        for i in range(NumberOfPopulation):
            #Calculate Probability
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
        NumberOfOnlooker = abc_parameters.ABCSetting.nOnlooker
        for i  in range (NumberOfOnlooker):
            # Select Source Site
            Source = self.RouletteWheelSelection(self)

            # New Bee Generation
            NewBee = population.Population() 
            
            # Comparision
            if (NewBee.CostValue <= self.ListOfPop[i].CostValue):
                self.ListOfPop[i] = NewBee
            else:
                self.ListOfPop[i].AbandonmentCounter = self.ListOfPop[i].AbandonmentCounter + 1
    
    @staticmethod
    def ScoutBees(self):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].AbandonmentCounter >= abc_parameters.ABCSetting.L):
                self.ListOfPop[i] = Population()
                self.ListOfPop[i].AbandonmentCounter = 0
    
    @staticmethod
    # Update Best Solution Ever Found
    def BestSolution(self):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].CostValue <= self.BestCost.CostValue):
                self.BestCost = self.ListOfPop[i]
                self.BestCostList.append(self.BestCost.CostValue)
                
    @staticmethod
    def ABCAlgorithm(self,Inbound,Outbound,LoadWeight,TimeStart):
        for i in range(abc_parameters.ABCSetting.MaxIt):
            self.CreateInitialPopulation(self,Inbound,Outbound,LoadWeight,TimeStart)
            self.RecruitedBees(self)
            self.CalculateFitness(self)
            self.OnlookerBees(self)
            self.ScoutBees(self)
            self.BestSolution(self)
        return self.BestCost