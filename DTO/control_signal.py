import DTO.road
import DTO.agv_car
import BLL.convert

class ControlSignal:
    def __init__(self,Road = ""):
        self.Road = Road
        self.Velocity = DTO.agv_car.AGVCar.MaxVelocity
        self.Action = 1
        self.waitTime = 0  # Thêm thuộc tính waitTime
        # self.Action = [0, 1, 2, 3, 4]

# 0 stop
# 1 go straight
# 2 turn right
# 3 turn left
# 4 reverse

    def __str__(self):
        return f"{self.Road.FirstNode} {self.Road.SecondNode} {self.Velocity} {self.Action}"



