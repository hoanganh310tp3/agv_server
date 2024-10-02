from . import map_execution
#Định nghĩa lớp MapTopology và các phương thức liên quan đến bản đồ.
class MapTopology:
    Map = map_execution.Map.returnMap()[0]
    Direction = map_execution.Map.returnMap()[1]
    def __init__(self):
        self.FeasiblePathFactor = map_execution.Map.returnFeasiblePathFactor(self.Map)
        
# MapTopology là một lớp đại diện cho bản đồ và các yếu tố liên quan đến bản đồ.
# Nó lưu trữ các thông tin về bản đồ, hướng di chuyển và các yếu tố khả thi cho các tuyến đường.
# Các phương thức trong lớp này được sử dụng để tính toán và quản lý các yếu tố này.
