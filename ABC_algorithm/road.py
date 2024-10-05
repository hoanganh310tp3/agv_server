# Đoạn code này định nghĩa lớp Road để biểu diễn một đoạn đường trong hệ thống AGV. Đây là phần quan trọng để mô phỏng các đường kết nối giữa các nút (node) trong bản đồ mà AGV sẽ di chuyển. Mỗi đoạn đường có hai nút đầu và cuối, một khoảng cách và một hướng di chuyển.

# Import các module cần thiết
from . import map_topology
from . import agv_car

class Road:
    # Khởi tạo đối tượng Road với các thuộc tính: nút đầu, nút cuối, khoảng cách và hướng
    def __init__(self, FirstNode=int(0), SecondNode=int(0), Distance=float(0), Direction=int(0)):
        self.FirstNode = FirstNode
        self.SecondNode = SecondNode
        self.Distance = Distance
        self.Direction = Direction

    # Phương thức tĩnh để lấy khoảng cách giữa hai nút từ bản đồ topology
#Code cũ của anh minh
    # @staticmethod
    # def GetDistance(PreviousNode, NextNode):
    #     return float(map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])

#Code mới 
    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    # Phương thức tĩnh để lấy hướng di chuyển giữa hai nút từ bản đồ topology
    @staticmethod
    def GetDirection(PreviousNode, NextNode):
        direction = map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)]
        return int(direction) if direction != '' else 0
 
    # Phương thức tĩnh để tạo danh sách các đối tượng Road từ danh sách các nút
    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = list()
        # Duyệt qua danh sách các nút và tạo đối tượng Road cho mỗi cặp nút liên tiếp
        for i in range(0, len(ListOfNode)-1):
            road = Road(ListOfNode[i], ListOfNode[i+1],   # Tạo đối tượng Road mới
                        Road.GetDistance(ListOfNode[i], ListOfNode[i+1]),  # Lấy khoảng cách
                        Road.GetDirection(ListOfNode[i], ListOfNode[i+1])) # Lấy hướng
            ListOfRoad.append(road)  # Thêm đối tượng Road vào danh sách
        return ListOfRoad  # Trả về danh sách các đối tượng Road


#ver 2
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
#         direction = map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)]
#         if direction == '':
#             return 0  # or some default value
#         return int(direction)
#         # return int(map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
 
#     @staticmethod
#     def returnListOfRoad(ListOfNode):
#         ListOfRoad = list()
#         for i in range(0, len(ListOfNode) - 1):
#             road = Road(ListOfNode[i], ListOfNode[i + 1], Road.GetDistance(ListOfNode[i], ListOfNode[i + 1]), Road.GetDirection(ListOfNode[i], ListOfNode[i + 1]))
#             ListOfRoad.append(road)
#         return ListOfRoad