import map_execution
#Định nghĩa lớp MapTopology và các phương thức liên quan đến bản đồ.
class MapTopology:
    Map = map_execution.Map.returnMap()[0]
    Direction = map_execution.Map.returnMap()[1]
    def __init__(self):
        self.FeasiblePathFactor = map_execution.Map.returnFeasiblePathFactor(self.Map)