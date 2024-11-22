import DTO.agv_car
import DTO.control_signal
#Tính toán năng lượng tiêu thụ của AGV.
class EnergyConsumption:   
    @staticmethod 
# Mục đích: Tính toán công suất dịch chuyển dựa trên gia tốc, vận tốc, và tải trọng của xe AGV.
# Công thức: P dịch chuyển = (trọng lượng xe AGV + trọng lượng hàng hóa) * (gia tốc + gia tốc trọng trường) * vận tốc
# Sử dụng các thuộc tính như trọng lượng AGV (AGVWeight), hệ số ma sát (nguy), và gia tốc trọng trường (g) để tính toán công suất dịch chuyển.
    def returnTranslatePower(Acceleration,Velocity,WeightLoad):
        TranslatePower = (DTO.agv_car.AGVCar.AGVWeight + WeightLoad)*(DTO.agv_car.AGVCar.nguy*DTO.agv_car.AGVCar.g + Acceleration)*Velocity
        return TranslatePower
    
    @staticmethod 
# Mục đích: Tính toán công suất động cơ dựa trên công suất dịch chuyển và hệ số ma sát của động cơ.
# Công thức: P động cơ = P dịch chuyển * (1 / hệ số ma sát của động cơ)
# Sử dụng hệ số ma sát của động cơ (nuyMotor) để tính toán công suất động cơ.
    def returnMotorPower(TranslatePower):
        MotorPower = TranslatePower*(1/DTO.agv_car.AGVCar.nuyMotor)
        return MotorPower
     
    @staticmethod 
# Mục đích: Tính toán năng lượng tiêu thụ trong quá trình tăng tốc của AGV.
# Công thức: E tăng tốc = tích phân công suất động cơ từ vận tốc ban đầu đến vận tốc đạt được trong quá trình tăng tốc.
# Sử dụng thời gian tăng tốc (AccelerationTime), gia tốc (Acceleration), và thời gian bước (Step) để tính toán năng lượng tiêu thụ.
#       Cách hoạt động:
# Tính thời gian tăng tốc dựa trên vận tốc hiện tại và vận tốc mục tiêu từ tín hiệu điều khiển.
# Dùng vòng lặp để tính công suất và năng lượng trong suốt quá trình tăng tốc.
# Tính tổng năng lượng tiêu thụ bằng cách cộng dồn năng lượng từ công suất động cơ trong mỗi bước thời gian.
    def returnAccelerationEnergy(RealVelocity,ControlSignal,WeightLoad):
        AccelerationTime = (float(ControlSignal.Velocity)-float(RealVelocity))/float(DTO.agv_car.AGVCar.MaxAccelaration)
        Acceleration = DTO.agv_car.AGVCar.MaxAccelaration + DTO.agv_car.AGVCar.nguy*DTO.agv_car.AGVCar.g
        i = 0
        Step = 0.01
        TotalMotorPower = 0
        TravelledDistance = 0
        while(i <= AccelerationTime):
            TotalMotorPower = TotalMotorPower + float(EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(Acceleration,RealVelocity,WeightLoad)))
            RealVelocity = RealVelocity + Acceleration*Step
            TravelledDistance = TravelledDistance + RealVelocity*Step
            i = Step + i
            
        TotalMotorEnergy = TotalMotorPower*Step + (float(ControlSignal.Road.Distance)-float(TravelledDistance))*EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(0,RealVelocity,WeightLoad))/RealVelocity
        return TotalMotorEnergy
    
    @staticmethod
# Mục đích: Tính toán năng lượng tiêu thụ trong quá trình duy trì vận tốc ổn định của AGV.
# Công thức: E ổn định = khoảng cách * công suất động cơ tại vận tốc ổn định / vận tốc ổn định
# Sử dụng vận tốc ổn định (ControlSignal.Velocity) và khoảng cách (ControlSignal.Road.Distance) để tính toán năng lượng tiêu thụ.
#    Cách hoạt động:
# Tính công suất động cơ khi xe không có gia tốc.
# Dùng công suất đó để tính tổng năng lượng tiêu thụ khi di chuyển một khoảng cách nhất định với vận tốc ổn định.
    def returnStableEnergy(ControlSignal,WeightLoad):
        TotalMotorEnergy = float(ControlSignal.Road.Distance)*EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(0,ControlSignal.Velocity,WeightLoad))/ControlSignal.Velocity
        return TotalMotorEnergy
    
    @staticmethod 
# Mục đích: Tính toán năng lượng tiêu thụ trong quá trình giảm tốc của AGV.
# Công thức: E giảm tốc = tích phân công suất động cơ từ vận tốc ban đầu đến vận tốc đạt được trong quá trình giảm tốc.
# Sử dụng thời gian giảm tốc (BrakingTime), gia tốc (BrakingAcceleration), và thời gian bước (Step) để tính toán năng lượng tiêu thụ.
#    Cách hoạt động:
# Tính thời gian giảm tốc dựa trên vận tốc hiện tại và vận tốc mục tiêu từ tín hiệu điều khiển.
# Dùng vòng lặp để tính công suất và năng lượng trong suốt quá trình giảm tốc.
# Tính tổng năng lượng tiêu thụ bằng cách cộng dồn năng lượng từ công suất động cơ trong mỗi bước thời gian.
    def returnBrakingEnergy(RealVelocity,ControlSignal,WeightLoad):
        AccelerationTime = (float(RealVelocity)-float(ControlSignal.Velocity))/float(DTO.agv_car.AGVCar.MinAccelaration)
        Acceleration = DTO.agv_car.AGVCar.MinAccelaration - DTO.agv_car.AGVCar.nguy*DTO.agv_car.AGVCar.g
        Step = 0.01
        i = 0
        TotalMotorPower = 0
        TravelledDistance = 0
        while(i <= AccelerationTime):
            TotalMotorPower = TotalMotorPower + EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(Acceleration,RealVelocity,WeightLoad))
            RealVelocity = RealVelocity + Acceleration*Step
            TravelledDistance = TravelledDistance + RealVelocity*Step
            i = Step + i
            
        TotalMotorEnergy = TotalMotorPower*Step + (float(ControlSignal.Road.Distance)-float(TravelledDistance))*EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(0,RealVelocity,WeightLoad))/RealVelocity
        return TotalMotorEnergy
    
    @staticmethod 
# Mục đích: Tính toán năng lượng tiêu thụ tổng cộng của AGV trong suốt quá trình di chuyển ( dựa trên danh sách các tín hiệu điều khiển).
# Công thức: E tổng = 2 * tổng năng lượng tiêu thụ trong quá trình tăng tốc và giảm tốc.
# Sử dụng các phương pháp trước đó để tính toán năng lượng tiêu thụ trong quá trình tăng tốc, giảm tốc và duy trì vận tốc ổn định.
#   Cách hoạt động:
# Duyệt qua danh sách các tín hiệu điều khiển.
# Tính năng lượng tiêu thụ trong quá trình tăng tốc, giảm tốc và duy trì vận tốc ổn định dựa trên từng tín hiệu điều khiển.
# Cộng dồn năng lượng tiêu thụ trong suốt quá trình di chuyển.
# Nhân kết quả với 2 để được năng lượng tiêu thụ tổng cộng  (có thể để bù đắp cho tổn thất năng lượng khác không được tính trong mô hình).
    def returnToTalEnergy(ListOfControlSignal,WeightLoad):
        TotalEnergy = float(0)
        RealVelocity = float(0)
        if(len(ListOfControlSignal) < 1):
            return float(100000)
        else:
            RealVelocity = 0
            for i in range(0,len(ListOfControlSignal)):
                if(ListOfControlSignal[i].Velocity > RealVelocity):
                    TotalEnergy = TotalEnergy + float(EnergyConsumption.returnAccelerationEnergy(RealVelocity,ListOfControlSignal[i],WeightLoad))
                elif(ListOfControlSignal[i].Velocity == RealVelocity):
                    TotalEnergy = TotalEnergy + float(EnergyConsumption.returnStableEnergy(ListOfControlSignal[i],WeightLoad))
                elif(ListOfControlSignal[i].Velocity < RealVelocity):
                    TotalEnergy = TotalEnergy + float(EnergyConsumption.returnBrakingEnergy(RealVelocity,ListOfControlSignal[i],WeightLoad))
                else:
                    break
                RealVelocity = ListOfControlSignal[i].Velocity
        return float(2)*TotalEnergy
    
# EnergyConsumption cung cấp các phương thức để tính toán năng lượng tiêu thụ cho AGV trong quá trình di chuyển.
# Nó tính toán năng lượng cho các giai đoạn tăng tốc, giữ vận tốc ổn định và giảm tốc, từ đó giúp dự đoán mức tiêu thụ năng lượng cho toàn bộ quá trình di chuyển.