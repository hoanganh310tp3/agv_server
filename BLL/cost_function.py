import BLL.map_execution
import BLL.constrains
import BLL.control_signal
import BLL.energy_consumption

class CostFunction:
    def returnCostFunction(ListOfControlSignal, LoadWeight):
        CostValue = BLL.energy_consumption.EnergyConsumption.returnToTalEnergy(ListOfControlSignal, LoadWeight)
        return CostValue
# CostFunction là một lớp định nghĩa các phương thức để tính toán giá trị hàm chi phí cho AGV.
# Nó sử dụng phương thức returnToTalEnergy của lớp EnergyConsumption để tính toán năng lượng tiêu thụ của AGV.
# Giá trị hàm chi phí được trả về là tổng năng lượng tiêu thụ của AGV.

