# from . import map_topology
# from . import agv_car


# class Road:
#     def __init__(self, FirstNode=int(0), SecondNode=int(0), Distance=float(0), Direction=int(0)):
#         self.FirstNode = FirstNode
#         self.SecondNode = SecondNode
#         self.Distance = Distance
#         self.Direction = Direction

#     @staticmethod
#     def GetDistance(PreviousNode, NextNode):
#         return float(map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
#     @staticmethod
#     def GetDirection(PreviousNode, NextNode):
#         return int(map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
 
#     @staticmethod
#     def returnListOfRoad(ListOfNode):
#         ListOfRoad = list()
#         for i in range(0, len(ListOfNode)-1):
#             road = Road(ListOfNode[i], ListOfNode[i+1],   #notice
#                         Road.GetDistance(ListOfNode[i], ListOfNode[i+1]), 
#                         Road.GetDirection(ListOfNode[i], ListOfNode[i+1]))
#             ListOfRoad.append(Road)
#         return ListOfRoad

from . import map_topology
from . import agv_car

class Road:
    def __init__(self, FirstNode=int(0), SecondNode=int(0), Distance=float(0), Direction=int(0)):
        self.FirstNode = FirstNode
        self.SecondNode = SecondNode
        self.Distance = Distance
        self.Direction = Direction

    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    @staticmethod
    def GetDirection(PreviousNode, NextNode):
        return int(map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
 
    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = list()
        for i in range(0, len(ListOfNode) - 1):
            road = Road(ListOfNode[i], ListOfNode[i + 1], Road.GetDistance(ListOfNode[i], ListOfNode[i + 1]), Road.GetDirection(ListOfNode[i], ListOfNode[i + 1]))
            ListOfRoad.append(road)
        return ListOfRoad