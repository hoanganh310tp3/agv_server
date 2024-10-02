from . import schedule
from . import position
from . import agv_car
from . import control_signal
from . import road
from . import convert
#Áp dụng các ràng buộc để đảm bảo an toàn và hiệu quả cho AGV
class Constrains:
# TimeStart: Thời gian bắt đầu di chuyển của AGV.
# Road: Đoạn đường mà AGV sẽ di chuyển, bao gồm các điểm FirstNode (điểm bắt đầu) và SecondNode (điểm kết thúc).
# Test: Chuyển đổi TimeStart từ định dạng timestamp sang thời gian thực để kiểm tra.
# ControlSignal: Tạo đối tượng ControlSignal để điều chỉnh tốc độ và hướng di chuyển của AGV.
    def CollisionConstrain(TimeStart,Road):
        Test = convert.Convert.returnTimeStampToTime(TimeStart)
        
        ControlSignal = control_signal.ControlSignal(Road)
        #Kiểm tra các lịch trình di chuyển khác
# Kiểm tra nếu có lịch trình di chuyển của các xe AGV khác trong hệ thống.
# Vòng lặp kiểm tra từng lịch trình EachSchedule để lấy vị trí của xe tại thời điểm TimeStart.
# Nếu returnPosition.FirstNode != "", có nghĩa là có xe AGV đang di chuyển trên đoạn đường liên quan, và cần kiểm tra các ràng buộc.
        
        if(len(schedule.Schedule.ListOfSchedule) > 0):
            for EachSchedule in schedule.Schedule.ListOfSchedule:
                returnPosition = position.Position.returnPosition(TimeStart,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain (ràng buộc đường đi)
# Kiểm tra nếu xe AGV đang đi theo hướng ngược lại với xe khác trên cùng một đoạn đường (Road.FirstNode == returnPosition.SecondNode và Road.SecondNode == returnPosition.FirstNode).
# Trong trường hợp này, xe AGV cần tránh va chạm bằng cách thiết lập tốc độ tối đa MaxVelocity và chuyển hướng đi (Road = road.Road(0, 0, 100000)).
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal
                    # Node constrain (ràng buộc về nút giao)
# Kiểm tra nếu xe đang đi cùng hướng với một xe khác trên cùng một đoạn đường và khoảng cách giữa chúng nhỏ hơn khoảng cách an toàn (SafetyDistance).
# Nếu có, tốc độ của xe sẽ được điều chỉnh dựa trên khoảng cách đã đi của xe phía trước để duy trì an toàn, tránh va chạm. 
                    # Similar direction
                    ControlSignal.Road = Road
                    if(Road.FirstNode == returnPosition.FirstNode and returnPosition.TravelledDistance < agv_car.AGVCar.SafetyDistance):
                        ControlSignal.Velocity = float(returnPosition.TravelledDistance)/(float(agv_car.AGVCar.SafetyDistance)*agv_car.AGVCar.MaxVelocity)
                        continue

                TimeEnd = TimeStart + Road.Distance/ControlSignal.Velocity
                # Middle point (Kiểm tra tại điểm giữa của đường)
# Tính toán thời gian di chuyển của xe TimeEnd dựa trên khoảng cách của đường và tốc độ hiện tại.
# Kiểm tra vị trí của các xe khác tại điểm giữa của đoạn đường. Nếu phát hiện va chạm tiềm năng tại điểm này, hệ thống sẽ điều chỉnh hướng và tốc độ của xe để tránh va chạm.             
                
                returnPosition = position.Position.returnPosition(TimeStart + (TimeEnd - TimeStart)/2,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal

                # End point(Kiểm tra tại điểm kết thúc của đường)
# Tương tự như kiểm tra điểm giữa, đoạn mã này kiểm tra vị trí của xe khác tại điểm gần cuối của đoạn đường. Nếu phát hiện nguy cơ va chạm, xe sẽ được điều chỉnh tốc độ và hướng đi.
                returnPosition = position.Position.returnPosition(TimeEnd-0.1,EachSchedule)
                if(returnPosition.FirstNode != ""):
                    # Path constrain
                    if(Road.FirstNode == returnPosition.SecondNode and Road.SecondNode == returnPosition.FirstNode):
                        ControlSignal.Road = road.Road(0,0,100000)
                        ControlSignal.Velocity = agv_car.AGVCar.MaxVelocity
                        return ControlSignal
                # Node constrain (Ràng buộc về nút giao tại điểm cuối) 
# Tính toán khoảng cách giữa xe hiện tại và xe phía trước tại điểm cuối của đoạn đường. Nếu khoảng cách nhỏ hơn khoảng cách an toàn, tốc độ sẽ được điều chỉnh để duy trì khoảng cách an toàn.   
                # Similar direction 
                ControlSignal.Road = Road
                if(Road.SecondNode == returnPosition.SecondNode and  Road.Distance - returnPosition.TravelledDistance  < agv_car.AGVCar.SafetyDistance):
                    ControlSignal.Velocity = round(Road.Distance/(float(Road.Distance - returnPosition.TravelledDistance + agv_car.AGVCar.SafetyDistance)/agv_car.AGVCar.MaxVelocity + float(Road.Distance)/agv_car.AGVCar.MaxVelocity),2)
                    continue
                # Different direction
                if(Road.SecondNode == returnPosition.FirstNode and (returnPosition.TravelledDistance < agv_car.AGVCar.SafetyDistance)):
                    ControlSignal.Velocity  = ControlSignal.Road.Distance*ControlSignal.Velocity/(agv_car.AGVCar.SafetyDistance - returnPosition.TravelledDistance + ControlSignal.Road.Distance)
                    continue
# Sau khi kiểm tra tất cả các ràng buộc, phương thức sẽ trả về đối tượng ControlSignal chứa thông tin về tốc độ và hướng đi an toàn cho AGV.
        return ControlSignal
    
# Phương thức CollisionConstrain trong lớp Constrains đảm bảo rằng AGV di chuyển an toàn và tránh va chạm với các xe khác bằng cách áp dụng các ràng buộc về tốc độ và hướng đi dựa trên vị trí hiện tại của các xe AGV khác trên cùng đoạn đường. Nếu phát hiện nguy cơ va chạm, phương thức sẽ điều chỉnh hướng và giảm tốc độ của AGV để đảm bảo an toàn.