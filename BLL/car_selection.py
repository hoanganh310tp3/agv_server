import BLL.requirement
import DTO.agv_car
import BLL.abc
import DTO.schedule
import DTO.population
import DTO.selected_car_trip
import BLL.convert
import DTO.requirement


# Loại bỏ import từ agv_management nếu đang cần test một mình thuật toán
from agv_management.active_agv import list_active_AGV

#Lựa chọn xe AGV dựa trên các yêu cầu và điều kiện.

class CarSelection:
    @staticmethod
    def InitialCar():
        try:
            aAGV = []
            DTO.agv_car.AGVCar.CarList = []
            aAGV = list_active_AGV()
            
            print(f"Active AGVs found: {aAGV}")  # Add this debug line
            
            if not aAGV:
                print("No active AGVs found")
                return False

            for eachCar in aAGV:
                NewCar = DTO.agv_car.AGVCar()
                NewCar.CarId = eachCar[0]
                NewCar.Location = eachCar[1]
                print(f"Initializing car: ID={eachCar[0]}, Location={eachCar[1]}")  # Add this debug line
                DTO.agv_car.AGVCar.CarList.append(NewCar)
            
            print(f"Total cars initialized: {len(DTO.agv_car.AGVCar.CarList)}")  # Add this debug line
            return True
                
        except Exception as e:
            print(f"Error initializing cars: {e}")
            return False

    
    # Phương thức này lựa chọn xe AGV dựa trên yêu cầu và điều kiện.
    # Nó tính toán thời gian trễ của mỗi xe AGV và chọn xe có thời gian trễ nhỏ hơn 120 giây.
    # Nếu thời gian trễ lớn hơn 120 giây, xe sẽ không được chọn.
    # Cuối cùng, nó sử dụng thuật toán ABC để lựa chọn xe AGV tốt nhất dựa trên yêu cầu và trọng số.
    @staticmethod
    def returnSelectedCar(Requirement):
        Weight = float(0)
    # Add 1 to account for 0-based indexing
        ListOfCar = [1]*(len(DTO.agv_car.AGVCar.CarList) + 1)
        TempList = [None]*(len(DTO.agv_car.AGVCar.CarList) + 1)
    
        for i in range(len(ListOfCar)):
            TempList[i] = Requirement.TimeStart
        
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = BLL.convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - BLL.convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
            else: 
                TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
# giải thích vòng lặp for
# Vòng lặp này duyệt qua danh sách các xe AGV đã khởi tạo:
# Nếu xe không có lịch trình (ScheduleList) thì bỏ qua.
# DelayTime: Tính thời gian trễ giữa kết thúc nhiệm vụ cuối cùng của xe và thời gian bắt đầu yêu cầu.
# Nếu thời gian trễ lớn hơn 120 phút, xe sẽ bị loại khỏi danh sách khả dụng (ListOfCar). Nếu không, cập nhật thời gian bắt đầu nhiệm vụ tiếp theo cho xe đó (TempList).
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(len(EachCar.ScheduleList) < 1):
                continue
            DelayTime = BLL.convert.Convert.TimeToTimeStamp(EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd) - BLL.convert.Convert.TimeToTimeStamp(Requirement.TimeStart)
            if(DelayTime > 0 ):
                if(DelayTime > 120):
                    ListOfCar[int(EachCar.CarId)] = 0
                else: 
                    TempList[int(EachCar.CarId)] = EachCar.ScheduleList[len(EachCar.ScheduleList)-1].TimeEnd
# NewABC: Tạo đối tượng ABC để sử dụng thuật toán Artificial Bee Colony nhằm tìm giải pháp tối ưu.
# BestCar: Lưu trữ thông tin về xe tốt nhất và chi phí tốt nhất.
# Vòng lặp duyệt qua các xe AGV khả dụng (ListOfCar) để tìm xe tốt nhất:
# Nếu vị trí hiện tại của xe trùng với điểm Inbound trong yêu cầu, chi phí sẽ bằng 0.
# Nếu không, thuật toán ABC được gọi để tính toán chi phí di chuyển từ vị trí hiện tại của xe đến điểm Inbound.
# Nếu chi phí của xe mới tìm thấy thấp hơn xe tốt nhất hiện tại, cập nhật BestCar với xe và chi phí mới.
        NewABC = BLL.abc.ABC()
        BestCar = DTO.selected_car_trip.SelectedCarTrip("",DTO.population.Population())
        for EachCar in DTO.agv_car.AGVCar.CarList:
            if(ListOfCar[int(EachCar.CarId)] == 1):
                TimeStart = BLL.convert.Convert.TimeToTimeStamp(TempList[EachCar.CarId])
                TempBestCost = DTO.population.Population()
                if(int(EachCar.Location) == int(Requirement.Inbound)):
                    TempBestCost.CostValue = 0
                else:
                    TempBestCost = NewABC.ABCAlgorithm(NewABC,int(EachCar.Location),int(Requirement.Inbound),Weight,TimeStart)
                if(TempBestCost.CostValue < BestCar.Cost.CostValue):
                    BestCar.Cost = TempBestCost
                    BestCar.Car = EachCar
# Cập nhật thời gian bắt đầu của yêu cầu theo thời gian khởi hành của xe tốt nhất đã chọn.
# return BestCar: Trả về xe AGV tốt nhất dựa trên các tiêu chí đã đánh giá.
        Requirement.TimeStart = TempList[int(BestCar.Car.CarId)]
        return BestCar
        