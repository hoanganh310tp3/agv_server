class AGVCar:
    delayTime = 30
    nuyMotor = float(0.625)
    nguy = float(0.0265)
    g = float(9.8)
    AGVWeight = float(17.155)#(kg)
    MaxVelocity = float(0.2)#(m/s)
    MaxAccelaration = float(1.5)#(m/s^2)
    MaxBatteryCapacity = float(432000)#(J)
    MinAccelaration = float(1)#(m/s^2)
    SafetyDistance = float(2)
    CarList = list()
    def __init__(self,CarId =""):
        self.CarId = CarId
        self.isAvailable = True
        self.ScheduleList = list()
        self.Location = ""
        self.BatteryCapacity = "100"
        self.CurrentPosition = ""

#Định nghĩa lớp AGVCar và các thuộc tính liên quan.