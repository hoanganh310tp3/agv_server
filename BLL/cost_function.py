import BLL.map_execution
import BLL.constrains
import BLL.control_signal
import BLL.energy_consumption
class CostFunction:
    def returnCostFunction(ListOfControlSignal, LoadWeight):
        CostValue = BLL.energy_consumption.EnergyConsumption.returnToTalEnergy(ListOfControlSignal, LoadWeight)
        return CostValue


