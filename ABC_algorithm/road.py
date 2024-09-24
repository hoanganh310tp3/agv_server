import map_topology
import agv_car

#Quản lý các thông tin liên quan đến đường đi của AGV.
class Road:
    def __init__(self, FirstNode=int(0), SecondNode=int(0), Distance=float(0), Direction=int(0)):
        self.FirstNode = FirstNode
        self.SecondNode = SecondNode
        self.Distance = Distance
        self.Direction = Direction

    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(Dto.MapTopology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    @staticmethod
    def GetDirection(PreviousNode, NextNode):
        return int(Dto.MapTopology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
 
    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = []
        for i in range(len(ListOfNode) - 1):
            road = Road(
                ListOfNode[i],
                ListOfNode[i+1],
                Road.GetDistance(ListOfNode[i], ListOfNode[i+1]),
                Road.GetDirection(ListOfNode[i], ListOfNode[i+1])
            )
            ListOfRoad.append(road)
        return ListOfRoad