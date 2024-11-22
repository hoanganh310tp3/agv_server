import BLL.map_execution

class MapTopology:
    Map = BLL.map_execution.Map.returnMap()[0]
    Direction = BLL.map_execution.Map.returnMap()[1]
    def __init__(self):
        self.FeasiblePathFactor = BLL.map_execution.Map.returnFeasiblePathFactor(self.Map)