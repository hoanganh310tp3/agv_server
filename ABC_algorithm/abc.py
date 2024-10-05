import numpy
from . import population
from . import abc_parameters
from . import cost_function
from . import map_execution


class ABC:
    def __init__(self):
        #Giải pháp có chi phí (cost) tốt nhất, được khởi tạo với một cá thể từ quần thể ban đầu.
        self.BestCost = population.Population() 
        #Danh sách chứa các cá thể (giải pháp) trong quần thể.
        self.ListOfPop = list()
        #Danh sách các giá trị fitness tương ứng với mỗi giải pháp trong quần thể.
        self.ListOfFitnessValue = [0]*abc_parameters.ABCSetting.nPop
        #Danh sách xác suất để chọn từng giải pháp dựa trên giá trị fitness của chúng.
        self.ListOfProbability = [0]*abc_parameters.ABCSetting.nPop
        #Danh sách lưu lại lịch sử các giá trị tốt nhất trong suốt quá trình chạy thuật toán.
        self.BestCostList = list()
        
    @staticmethod
# Hàm này tính toán giá trị của hàm chi phí (cost function) cho một giải pháp.
# Nếu kết nối cuối cùng của giải pháp không phù hợp với mục tiêu đầu ra (Outbound), nó trả về một giá trị chi phí rất lớn (100000), coi như giải pháp không hợp lệ.
# Nếu hợp lệ, nó sử dụng một hàm khác từ mô-đun cost_function để tính toán giá trị chi phí thực tế.
    def returnCostFunction(ListOfControlSignal,Outbound,LoadWeight):
        CostFunctionValue = float(0)
        
        if(int(ListOfControlSignal[len(ListOfControlSignal)-int(1)].Road.SecondNode) != int(Outbound)):
            return float(100000)
        else:    
            CostFunctionValue = cost_function.CostFunction.returnCostFunction(ListOfControlSignal,LoadWeight)
        return CostFunctionValue
    
    @staticmethod
# Hàm này tạo quần thể ban đầu gồm nPop giải pháp.
# Mỗi giải pháp được tạo bằng cách khởi tạo các cá thể của lớp Population, với các thông tin đầu vào như điểm xuất phát (Inbound), điểm đến (Outbound), trọng lượng tải (LoadWeight), và thời gian bắt đầu (TimeStart).
# Nếu một giải pháp mới có chi phí tốt hơn giải pháp tốt nhất hiện tại, nó sẽ được lưu vào self.BestCost.
    # Đang test nên tạm thời comment out ràng buộc lập lịch
    # def CreateInitialPopulation(self,Inbound,Outbound,LoadWeigth,TimeStart):
    def CreateInitialPopulation(self,Inbound,Outbound,LoadWeigth,TimeStart, ignore_scheduling=False):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop 
        for i in range (NumberOfPopulation):
            NewPop = population.Population(Inbound,Outbound,LoadWeigth,TimeStart, ignore_scheduling)
            if(self.BestCost.CostValue >= NewPop.CostValue):
                self.BestCostList.append(self.BestCost.CostValue)
                self.BestCost = NewPop
            self.ListOfPop.append(NewPop)
    
    @staticmethod
        # Ở giai đoạn này, các con ong làm việc tạo ra các giải pháp mới ngẫu nhiên.
        # Nếu giải pháp mới tốt hơn giải pháp hiện tại, nó sẽ thay thế giải pháp cũ. Nếu không, bộ đếm số lần không cải thiện của giải pháp đó tăng lên (AbandonmentCounter).
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
# Hàm này tính toán giá trị fitness cho từng giải pháp dựa trên chi phí của chúng.
# Fitness được tính bằng công thức 1 / (1 + cost), giá trị này càng lớn khi chi phí càng nhỏ.
# Sau đó, xác suất chọn từng giải pháp sẽ được tính dựa trên giá trị fitness.
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
# Hàm này sử dụng phương pháp Roulette Wheel Selection để chọn ngẫu nhiên một giải pháp dựa trên xác suất đã tính toán.
# Nó sinh ra một số ngẫu nhiên và kiểm tra xem giải pháp nào sẽ được chọn dựa trên xác suất tích lũy. 
    def RouletteWheelSelection(self):
        RandomNumber = numpy.random.uniform(0,1)
        Probability = self.ListOfProbability[0]
        for i in range (len(self.ListOfProbability)):
            if(RandomNumber < Probability):
                return int(i)
            else:
                Probability = Probability + self.ListOfProbability[i]
                
    @staticmethod
# Ở giai đoạn này, các con ong quan sát chọn giải pháp dựa trên xác suất và sinh ra các giải pháp mới.
# Tương tự như ong làm việc, nếu giải pháp mới tốt hơn, nó sẽ thay thế giải pháp cũ.
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
# Nếu một giải pháp không được cải thiện sau một số lần lặp nhất định (quá giới hạn L), giải pháp đó sẽ bị loại bỏ và tạo ra giải pháp mới.
    def ScoutBees(self):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].AbandonmentCounter >= abc_parameters.ABCSetting.L):
                self.ListOfPop[i] = population.Population()
                self.ListOfPop[i].AbandonmentCounter = 0
    
    @staticmethod
# Sau mỗi vòng lặp, hàm này kiểm tra và cập nhật giải pháp tốt nhất trong quần thể.   
    # Update Best Solution Ever Found
    def BestSolution(self):
        NumberOfPopulation = abc_parameters.ABCSetting.nPop
        for i in range (NumberOfPopulation):
            if (self.ListOfPop[i].CostValue <= self.BestCost.CostValue):
                self.BestCost = self.ListOfPop[i]
                self.BestCostList.append(self.BestCost.CostValue)
    
    @staticmethod
# Hàm này là nơi thuật toán ABC được thực thi đầy đủ. Nó lặp qua các giai đoạn "ong làm việc", "ong quan sát", "ong trinh sát" và cập nhật giải pháp tốt nhất.
# Sau khi đạt đến số lần lặp tối đa (MaxIt), nó trả về giải pháp tốt nhất tìm được.
    # Đang test nên tạm thời comment out ràng buộc lập lịch
    # def ABCAlgorithm(self,Inbound,Outbound,LoadWeight,TimeStart):
    def ABCAlgorithm(self, Inbound, Outbound, LoadWeight, TimeStart, ignore_scheduling=False):
        for i in range(abc_parameters.ABCSetting.MaxIt):
            self.CreateInitialPopulation(self,Inbound,Outbound,LoadWeight,TimeStart, ignore_scheduling)
            self.RecruitedBees(self)
            self.CalculateFitness(self)
            self.OnlookerBees(self)
            self.ScoutBees(self)
            self.BestSolution(self)
        return self.BestCost
  