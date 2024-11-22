class Requirement:
    def __init__(self,Order="",Name="",Number = "",Weight="",TimeStart="",Inbound="",Outbound="", CalledCar ="", Date =""):
        self.Order = Order
        self.Name = Name
        self.CalledCar = CalledCar
        self.Date = Date
        self.LoadWeight = 0
        self.TimeStart = TimeStart
        self.Inbound = Inbound
        self.Outbound = Outbound
        self.Number = 0
    
    def __str__(self):
        return f"{self.Order}, {self.Date}, {self.Name}, {self.CalledCar}, {self.Inbound}, {self.Outbound}"