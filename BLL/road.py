import DTO.map_topology
import DTO.road
import BLL.road
import DTO.agv_car          

class Road:
    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(DTO.map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    def GetDirection(PreviousNode, NextNode):
        return int(DTO.map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
    
    # hướng đông = 2
    # hướng tây = 4
    # hướng nam = 3
    # hướng bắc = 1
    # vô hướng = 5
    
    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = list()
        for i in range(0, len(ListOfNode)-1):
            UnProcessedDirection1 = BLL.road.Road.GetDirection(ListOfNode[i], ListOfNode[i+1])
            
            # For the last road segment, maintain the previous ProcessedDirection
            if i == len(ListOfNode)-2:
                # Skip direction processing for last segment
                ProcessedDirection = 0
            else:
                UnProcessedDirection2 = BLL.road.Road.GetDirection(ListOfNode[i+1], ListOfNode[i+2])
            
            # Process directions only for non-last segments
            if UnProcessedDirection2 == UnProcessedDirection1:
                ProcessedDirection = 1
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 4:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 3:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 1:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 2:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 3:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 1:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 2:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 4:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 1:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 2:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 4:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 3:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 5 or UnProcessedDirection2 == 5:
                ProcessedDirection = 0
            else:
                pass
            Road = DTO.road.Road(ListOfNode[i],ListOfNode[i+1],BLL.road.Road.GetDistance(ListOfNode[i],ListOfNode[i+1]), ProcessedDirection)
            ListOfRoad.append(Road)
        return ListOfRoad
