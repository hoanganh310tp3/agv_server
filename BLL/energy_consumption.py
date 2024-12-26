import DTO.agv_car
import DTO.control_signal
class EnergyConsumption:   
    @staticmethod 
    def returnTranslatePower(Acceleration,Velocity,WeightLoad):
        TranslatePower = (DTO.agv_car.AGVCar.AGVWeight + WeightLoad)*(DTO.agv_car.AGVCar.nguy*DTO.agv_car.AGVCar.g + Acceleration)*Velocity
        return TranslatePower
    
    @staticmethod 
    def returnMotorPower(TranslatePower):
        MotorPower = TranslatePower*(1/DTO.agv_car.AGVCar.nuyMotor)
        return MotorPower
     
    @staticmethod 
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
    def returnStableEnergy(ControlSignal,WeightLoad):
        TotalMotorEnergy = float(ControlSignal.Road.Distance)*EnergyConsumption.returnMotorPower(EnergyConsumption.returnTranslatePower(0,ControlSignal.Velocity,WeightLoad))/ControlSignal.Velocity
        return TotalMotorEnergy
    
    @staticmethod 
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