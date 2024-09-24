import ABC_algorithm.convert 
#Gửi các tín hiệu điều khiển và dữ liệu liên quan đến AGV.
class Send:
    def get_control_signal_bytes(Schedule):
        print(Schedule.ListOfControlSignal)
        ListOfByteControlSignal = bytearray()
        ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(122,1) + ABC_algorithm.convert.Convert.returnIntToByte(3,1)
        for EachControlSignal in Schedule.ListOfControlSignal:
            ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(EachControlSignal.Road.FirstNode,2) + ABC_algorithm.convert.Convert.returnFloatToByte(EachControlSignal.Velocity,1) + ABC_algorithm.convert.Convert.returnFloatToByte(EachControlSignal.Road.Distance,2) + ABC_algorithm.convert.Convert.returnIntToByte(EachControlSignal.Action,1)
        Length = len(Schedule.ListOfControlSignal)
        ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(Schedule.ListOfControlSignal[Length-1].Road.SecondNode,2) + ABC_algorithm.convert.Convert.returnFloatToByte(Schedule.ListOfControlSignal[Length-1].Velocity,1) + ABC_algorithm.convert.Convert.returnFloatToByte(Schedule.ListOfControlSignal[Length-1].Road.Distance,2) + ABC_algorithm.convert.Convert.returnIntToByte(Schedule.ListOfControlSignal[Length-1].Action,1)
        ListOfByteControlSignal = ListOfByteControlSignal + ABC_algorithm.convert.Convert.returnIntToByte(127,1)
        return ListOfByteControlSignal

    def SendToUI(Schedule):
        TotalDistance = float(0)
        TempString = ""
        TempString = TempString + str(Schedule.Order)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.Name)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.Car.CarId)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.BatteryCapacity)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.TotalEnergy)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.LoadWeight)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.TimeStart)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.TimeEnd)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.Inbound)
        TempString = TempString + ","
        TempString = TempString + str(Schedule.Outbound)
        TempString = TempString + ","
        for EachControlSignal in Schedule.ListOfControlSignal:
            TotalDistance = TotalDistance + EachControlSignal.Road.Distance
        TempString = TempString + str(TotalDistance)
        TempString = TempString + ","
        for EachControlSignal in Schedule.ListOfControlSignal:
            TempString = TempString + str(EachControlSignal.Road.FirstNode)
            TempString = TempString + str(EachControlSignal.Road.SecondNode)
            TempString = TempString + "("+ str(EachControlSignal.Road.Distance) +" m)"
            TempString = TempString + "("+ str(EachControlSignal.Velocity) +" m/s)"
            TempString = TempString + ","
        TempString = TempString + "\n"
        return TempString