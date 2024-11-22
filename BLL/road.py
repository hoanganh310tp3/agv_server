# Đoạn code này định nghĩa lớp Road để biểu diễn một đoạn đường trong hệ thống AGV. Đây là phần quan trọng để mô phỏng các đường kết nối giữa các nút (node) trong bản đồ mà AGV sẽ di chuyển. Mỗi đoạn đường có hai nút đầu và cuối, một khoảng cách và một hướng di chuyển.

# Import các module cần thiết
import DTO.map_topology
import DTO.road
import BLL.road
import DTO.agv_car          

class Road:
    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(DTO.map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    # Phương thức tĩnh để lấy hướng di chuyển giữa hai nút từ bản đồ topology
    def GetDirection(PreviousNode, NextNode):
        return int(DTO.map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
    
    # Phương thức tĩnh để tạo danh sách các đối tượng Road từ danh sách các nút
    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = list()
        for i in range(0,len(ListOfNode)-1):
            Road = DTO.road.Road(ListOfNode[i],ListOfNode[i+1],BLL.road.Road.GetDistance(ListOfNode[i],ListOfNode[i+1]), BLL.road.Road.GetDirection(ListOfNode[i],ListOfNode[i+1]))
            ListOfRoad.append(Road)
        return ListOfRoad

