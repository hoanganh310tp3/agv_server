from . import agv_car
from . import convert
from . import abc
from . import requirement
from . import car_selection
#Đoạn code này định nghĩa lớp Schedule để quản lý lịch trình vận chuyển của các xe AGV, bao gồm việc tính toán và tạo ra lịch trình cho các yêu cầu vận chuyển.
class Schedule:
    ListOfSchedule = list()
#Khởi tạo một đối tượng Schedule với các thuộc tính như: danh sách tín hiệu điều khiển, đơn hàng, ngày tháng, thông tin xe, năng lượng tiêu thụ, khoảng cách, thời gian bắt đầu và kết thúc, cùng với thông tin vào và ra của yêu cầu vận chuyển
    def __init__(self):
        self.ListOfControlSignal = list()
        self.Order = ""
        self.Date = ""
        self.Name = "Transporting"
        self.LoadAmount = 0
        self.LoadWeight = 0
        self.Car = ""
        self.BatteryCapacity = ""
        self.TotalEnergy = 0
        self.TotalDistance = 0
        self.TimeStart = ""
        self.TimeEnd = ""
        self.Inbound = ""
        self.Outbound = ""
        self.ControlSignal = ""

    @staticmethod
    def returnSchedule(Requirement, SelectedCarTrip, SelectedTransportingTrip):
        # Tạo một đối tượng Schedule mới
        Schedule = Schedule()
        # Gán các thuộc tính của đối tượng Schedule từ Requirement và SelectedCarTrip
        Schedule.Name = Requirement.Name
        Schedule.Order = Requirement.Order
        Schedule.Date = Requirement.Date
        Schedule.Car = SelectedCarTrip.Car
        Schedule.Car.Location = Requirement.Outbound
        Schedule.Inbound = Requirement.Inbound
        Schedule.Outbound = Requirement.Outbound
        Schedule.TimeStart = Requirement.TimeStart
        Schedule.LoadWeight = Requirement.LoadWeight
        # Kết hợp danh sách các tín hiệu điều khiển từ SelectedCarTrip và SelectedTransportingTrip
        Schedule.ListOfControlSignal = SelectedCarTrip.Cost.ListOfControlSignal + SelectedTransportingTrip.ListOfControlSignal
        # Tính toán thời gian kết thúc của lịch trình
        Schedule.TimeEnd = convert.Convert.returnTimeStampToTime(convert.Convert.TimeToTimeStamp(Schedule.TimeStart) + convert.Convert.returnScheduleToTravellingTime(Schedule.ListOfControlSignal) + agv_car.AGVCar.delayTime)
        # Tính toán tổng năng lượng tiêu thụ
        Schedule.TotalEnergy = round(SelectedCarTrip.Cost.CostValue + SelectedTransportingTrip.CostValue, 3)
        # Cập nhật dung lượng pin của xe
        Schedule.Car.BatteryCapacity = round((float(Schedule.Car.BatteryCapacity)*agv_car.AGVCar.MaxBatteryCapacity/100 - float(Schedule.TotalEnergy))*float(100)/(agv_car.AGVCar.MaxBatteryCapacity), 2)
        Schedule.BatteryCapacity = Schedule.Car.BatteryCapacity
        # Thêm lịch trình vào danh sách lịch trình của xe
        Schedule.Car.ScheduleList.append(Schedule)
        return Schedule
    
    @staticmethod
    def returnListOfSchedule():
        # Đọc danh sách các yêu cầu từ bảng thời gian
        ListOfRequirement = requirement.Requirement.ReadTimeTable()
        # Khởi tạo danh sách các xe
        car_selection.CarSelection.InitialCar()
        # Duyệt qua từng yêu cầu trong danh sách
        for EachRequirement in ListOfRequirement:
            # Tạo một đối tượng ABC mới
            NewABC = abc.ABC()
            # Lựa chọn xe phù hợp cho yêu cầu
            SelectedCarTrip = car_selection.CarSelection.returnSelectedCar(EachRequirement)
            TimeStart = convert.Convert.TimeToTimeStamp(EachRequirement.TimeStart)
            # Nếu có nhiều hơn một tín hiệu điều khiển, tính toán thời gian bắt đầu mới
            if len(SelectedCarTrip.Cost.ListOfControlSignal) > 1:
                TimeStart = convert.Convert.returnScheduleToTravellingTime(SelectedCarTrip.Cost.ListOfControlSignal) + TimeStart
            # Tạo chuyến đi vận chuyển bằng thuật toán ABC
            SelectedTransportingTrip = NewABC.ABCAlgorithm(NewABC, EachRequirement.Inbound, EachRequirement.Outbound, EachRequirement.LoadWeight, TimeStart)
            # Tạo lịch trình cho yêu cầu
            Schedule = Schedule.returnSchedule(EachRequirement, SelectedCarTrip, SelectedTransportingTrip)
            # Thêm lịch trình vào danh sách lịch trình
            Schedule.ListOfSchedule.append(Schedule)

    @staticmethod
    def return_to_lot(startNode, stopNode, loadWeight, timeStart):
        # Tạo một đối tượng ABC mới
        NewABC = abc.ABC()
        # Tạo lộ trình quay lại bãi bằng thuật toán ABC
        Route = NewABC.ABCAlgorithm(NewABC, startNode, stopNode, loadWeight, timeStart)
        return Route

    def get_car_id(self):
        # Trả về ID của xe
        return self.Car.CarId # notice

    def get_total_distance(self):
        # Tính tổng khoảng cách của tất cả các tín hiệu điều khiển trong danh sách
        return sum(EachControlSignal.Road.Distance for EachControlSignal in self.ListOfControlSignal)
      
    def list_control_signal(self):
        # Tạo danh sách các tín hiệu điều khiển
        ControlSignal = [self.get_car_id()]
        for EachControlSignal in self.ListOfControlSignal:
            # Thêm thông tin của từng tín hiệu điều khiển vào danh sách
            ControlSignal.append([EachControlSignal.Road.FirstNode, EachControlSignal.Road.SecondNode, EachControlSignal.Velocity, EachControlSignal.Road.Distance, EachControlSignal.Road.Direction])
        
        # Thêm tín hiệu điều khiển cuối cùng vào danh sách
        last_control_signal = self.ListOfControlSignal[-1]
        ControlSignal.append([last_control_signal.Road.SecondNode, last_control_signal.Road.SecondNode, 0, 0, 0])
        return ControlSignal