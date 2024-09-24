import numpy
import abc_parameters
import environ
#Xử lý bản đồ và các yếu tố liên quan đến đường đi.
env = environ.Env()
environ.Env.read_env()

class Map:
    @staticmethod
    def returnFeasiblePathFactor(RoadList):
        Length = len(RoadList)
        FeasibleFactor = numpy.empty((Length, Length)) 
        for i in range(Length):
            Count = float(0)
            for j in range(Length):
                if(float(RoadList[i][j]) != 100000 and float(RoadList[i][j]) != 0):
                    Count = Count +1   
            for j in range(Length):
                if(float(RoadList[i][j]) != 100000 and float(RoadList[i][j]) != 0):
                    FeasibleFactor[i][j] = 100/float(Count)
                else:
                    FeasibleFactor[i][j] = 0
        return FeasibleFactor
    
    @staticmethod
    def returnMap():
        f = open('Map3_test.csv','r')
        RoadList = list()
        for line in f:
            RoadList.append(list(line.strip().split(',')))
        f.close()

        NodeList = list()
        DirectionList = list()

        for eachLine in RoadList:
            NodeLine = list()
            DirectionLine = list()
            for eachNode in eachLine:
                NodeLine.append(str(eachNode).split(';')[0])
                DirectionLine.append(str(eachNode).split(';')[1])
            NodeList.append(NodeLine)
            DirectionList.append(DirectionLine)
        
        return (NodeList, DirectionList)

    @staticmethod
    def returnFeasiblePath(Inbound, Outbound):
        RoadList = Map.returnMap()[0]
        FeasibleFactor = Map.returnFeasiblePathFactor(RoadList)
        Count = int(0)
        TravelledNode = list()
        TravelledNode.append(int(Inbound))
        CurrentNode = int(Inbound)
        HighPoint = float(100)
        while (CurrentNode != int(Outbound)):
            Count = Count + 1
            if(Count == abc_parameters.ABCSetting.nCount):  # Thay thế bằng ABCSetting.nCount nếu cần
                return TravelledNode
            Flag = bool(False)
            RandomNumber = numpy.random.uniform(1,HighPoint)
            Probability = FeasibleFactor[CurrentNode][0]
            for j in range (0,len(RoadList)):
                if(RandomNumber < Probability):
                    CurrentNode = j
                    TravelledNode.append(int(j))
                    Flag = True
                    HighPoint = 100
                    for Element in TravelledNode:
                        FeasibleFactor[j][Element] = 0
                    break
                else:
                    if(int(j) < len(RoadList) -1 ):
                        Probability  = Probability + FeasibleFactor[CurrentNode][j+1]
            if(Flag == False):
                HighPoint = RandomNumber
                continue
        return TravelledNode