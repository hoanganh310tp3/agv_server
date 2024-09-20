import energy_consumption

class CostFunction:
    @staticmethod
    def returnCostFunction(ListOfControlSignal, LoadWeight):
        CostValue = energy_consumption.EnergyConsumption.returnToTalEnergy(ListOfControlSignal, LoadWeight)
        return CostValue