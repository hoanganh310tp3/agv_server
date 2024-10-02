from . import road
from . import agv_car
from . import constrains
#Tạo và quản lý các tín hiệu điều khiển cho AGV.
class ControlSignal:
# Road: Thông tin về đoạn đường mà xe AGV sẽ di chuyển. Nếu không có đoạn đường nào được cung cấp, giá trị mặc định là một chuỗi rỗng.
# Velocity: Tốc độ di chuyển của AGV, khởi tạo với tốc độ tối đa từ AGVCar.MaxVelocity.
# Action: Mã hành động của AGV. Mặc định là 1, đại diện cho việc di chuyển thẳng (go straight).   
    def __init__(self, Road=""):
        self.Road = Road
        self.Velocity = agv_car.AGVCar.MaxVelocity
        self.Action = 1
# Phương thức này được sử dụng để trả về một chuỗi biểu diễn đối tượng ControlSignal, gồm:

# FirstNode và SecondNode: Các điểm đầu và cuối của đoạn đường.
# Velocity: Tốc độ hiện tại của AGV.
# Action: Mã hành động của AGV.
# Ví dụ, nếu đoạn đường là từ node 1 đến node 2, tốc độ là 5 m/s và hành động là di chuyển thẳng, thì chuỗi trả về sẽ như sau: "1 2 5 1"
    def __str__(self):
        return f"{self.Road.FirstNode} {self.Road.SecondNode} {self.Velocity} {self.Action}"

    @staticmethod
# TimeStart: Thời gian bắt đầu di chuyển.
# ListOfNode: Danh sách các node mà AGV sẽ đi qua (các điểm trên đường di chuyển của AGV).
# ListOfRoad: Được tạo bằng cách chuyển đổi danh sách các node thành danh sách các đoạn đường mà AGV sẽ đi qua.
    def returnListOfControlSignal(TimeStart, ListOfNode):
        ListOfControlSignal = list()
        ListOfRoad = road.Road.returnListOfRoad(ListOfNode)
        
# Với mỗi đoạn đường trong ListOfRoad, phương thức sẽ kiểm tra ràng buộc về va chạm thông qua hàm CollisionConstrain của lớp Constrains.
# Kết quả kiểm tra sẽ trả về một đối tượng ControlSignal với thông tin về tốc độ và hướng di chuyển của AGV, và kết quả này sẽ được thêm vào danh sách ListOfControlSignal.
        for EachRoad in ListOfRoad:
            signal = constrains.Constrains.CollisionConstrain(TimeStart, EachRoad)
            ListOfControlSignal.append(signal)
    # Mỗi tín hiệu điều khiển trong ListOfControlSignal được điều chỉnh tốc độ dựa trên các ràng buộc đã kiểm tra:
# Nếu tốc độ vượt quá MaxVelocity, tốc độ sẽ bị giới hạn ở mức MaxVelocity (tốc độ tối đa).
# Nếu tốc độ nằm trong các khoảng từ 0.1 m/s đến 0.2 m/s, thì tốc độ sẽ bị điều chỉnh về các giá trị tương ứng (0.1, 0.15, 0.20).
# Nếu tốc độ nhỏ hơn 0.1 m/s, tốc độ sẽ bị giới hạn ở mức 0.1 m/s.        
        for Element in ListOfControlSignal:
            if Element.Velocity >= agv_car.AGVCar.MaxVelocity:
                Element.Velocity = agv_car.AGVCar.MaxVelocity
            elif Element.Velocity >= 0.20:
                Element.Velocity = 0.20
            elif Element.Velocity >= 0.15:
                Element.Velocity = 0.15
            elif Element.Velocity >= 0.1:
                Element.Velocity = 0.1
            else:
                Element.Velocity = 0.1
# Sau khi tất cả các tín hiệu điều khiển được điều chỉnh, danh sách ListOfControlSignal được trả về, chứa các tín hiệu cần thiết để điều khiển xe AGV trên toàn bộ hành trình.
        return ListOfControlSignal

# 0 stop
# 1 go straight
# 2 turn right
# 3 turn left
# 4 reverse

# Lớp ControlSignal quản lý tín hiệu điều khiển của AGV, bao gồm tốc độ và hành động của xe.
# Tốc độ và hướng di chuyển của AGV được điều chỉnh dựa trên các ràng buộc về va chạm để đảm bảo an toàn.
# Tốc độ của xe sẽ được điều chỉnh về các giá trị hợp lý (tối đa hoặc các mức an toàn nhỏ hơn).