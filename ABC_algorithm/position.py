from . import schedule
from . import road
from . import convert

# Position là một lớp định nghĩa các thuộc tính và phương thức để quản lý vị trí của AGV.
# Các thuộc tính:
# FirstNode: Nút đầu tiên trong đường đi mà AGV đang di chuyển.
# SecondNode: Nút thứ hai trong đường đi mà AGV đang di chuyển.
# TravelledDistance: Khoảng cách đã đi được. Khoảng cách AGV đã di chuyển tính từ FirstNode tại thời điểm cho trước.
# Car: xe AGV hiện tại đang hoạt động.
# Velocity: Tốc độ của xe.
# Các phương thức:
# __init__: Phương thức khởi tạo, được sử dụng để khởi tạo các thuộc tính của lớp.
# returnPosition: Phương thức tính toán vị trí của xe tại thời điểm Time.

class Position:
    def __init__(self):
        self.FirstNode = ""
        self.SecondNode = ""
        self.TravelledDistance = ""
        self.Car = ""
        self.Velocity = ""

    @staticmethod 
#     Chức năng:
# Phương thức này trả về vị trí của AGV tại một thời điểm cụ thể Time dựa trên lịch trình của AGV (được cung cấp qua Schedule).

#    Giải thích chi tiết:
#    1.Khởi tạo vị trí:
# position = Position(): Tạo một đối tượng Position rỗng để lưu thông tin về vị trí của xe AGV.
#    2.Tính toán thời gian:
# TimeCounter = convert.Convert.TimeToTimeStamp(Schedule.TimeStart): Chuyển thời gian bắt đầu từ Schedule sang định dạng timestamp để dễ dàng tính toán.
# TimeEnd = convert.Convert.TimeToTimeStamp(Schedule.TimeEnd): Chuyển thời gian kết thúc của lịch trình thành timestamp.
#    3.Vòng lặp kiểm tra các đoạn đường:
# while TimeCounter <= TimeEnd:: Tiếp tục lặp cho đến khi thời gian hiện tại của lộ trình vượt qua thời điểm kết thúc.
#    Trong mỗi lần lặp:
# Distance = Schedule.ListOfControlSignal[Index].Road.Distance: Lấy khoảng cách của đoạn đường hiện tại.
# Velocity = Schedule.ListOfControlSignal[Index].Velocity: Lấy vận tốc của AGV trên đoạn đường hiện tại.
#    4.Xác định vị trí AGV:
# if TimeCounter + Distance / Velocity > Time:: Nếu AGV vẫn đang di chuyển trên đoạn đường này tại thời điểm Time, tính toán vị trí AGV.
# position.FirstNode và position.SecondNode: Lấy thông tin về các nút đầu và cuối của đoạn đường.
# position.TravelledDistance: Tính khoảng cách AGV đã di chuyển từ FirstNode tại thời điểm Time.
# position.Car và position.Velocity: Gán xe và vận tốc của AGV.
#    5.Tăng chỉ số lộ trình:
# Index += 1: Di chuyển đến đoạn đường tiếp theo trong Schedule.ListOfControlSignal.
# TimeCounter += Distance / Velocity: Cập nhật thời gian của lộ trình dựa trên khoảng cách và vận tốc.
#    6.Trả về đối tượng Position:
# Nếu tìm thấy vị trí AGV tại thời điểm Time, hàm trả về đối tượng position với các giá trị đã tính toán.
# Nếu không tìm thấy, đối tượng position sẽ có các giá trị rỗng và được trả về mặc định.
    def returnPosition(Time, Schedule):
        position = Position()
        TimeCounter = convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
        Index = 0
        TimeEnd = convert.Convert.TimeToTimeStamp(Schedule.TimeEnd)
        while TimeCounter <= TimeEnd:
            Distance = Schedule.ListOfControlSignal[Index].Road.Distance
            Velocity = Schedule.ListOfControlSignal[Index].Velocity
            if TimeCounter + Distance / Velocity > Time:
                position.FirstNode = Schedule.ListOfControlSignal[Index].Road.FirstNode
                position.SecondNode = Schedule.ListOfControlSignal[Index].Road.SecondNode
                position.TravelledDistance = float(Velocity) * (Time - TimeCounter)
                position.Car = Schedule.Car
                position.Velocity = Schedule.Car
                return position
            Index += 1
            if Index == len(Schedule.ListOfControlSignal):
                break
            TimeCounter += Distance / Velocity 
        return position
# Phương thức returnPosition dùng để tính toán và trả về vị trí của AGV (bao gồm hai nút đầu, cuối, khoảng cách đã di chuyển và vận tốc) tại một thời điểm xác định dựa trên lịch trình.