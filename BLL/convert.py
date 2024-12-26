from datetime import datetime

class Convert:  
    @staticmethod
    def TimeToTimeStamp(Time):
        if isinstance(Time, float):
            return Time
        Temp = Time.split(":")
        Date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(Temp[0]), int(Temp[1]), int(Temp[2]))
        return datetime.timestamp(Date)
    
    @staticmethod
    def returnCorrectFormTime(Time):
        if(int(Time)<10):
            return "0" + str(Time)
        return str(Time) 
    
    @staticmethod 
    def returnScheduleToTravellingTime(ListOfControlSignal):
        TravellingTime = float(0)
        for EachControlSignal in ListOfControlSignal:
            TravellingTime = TravellingTime + float(EachControlSignal.Road.Distance)/float(EachControlSignal.Velocity)
        return TravellingTime
    
    @staticmethod 
    def returnTimeStampToTime(TimeStamp):
        Time = datetime.fromtimestamp(TimeStamp)
        CorrectTime = Convert.returnCorrectFormTime(Time.hour) + ":" + Convert.returnCorrectFormTime(Time.minute) + ":" + Convert.returnCorrectFormTime(Time.second)
        return CorrectTime
    
    @staticmethod 
    def returnIntToByte(Value,NumberOfByte):
        Value = int(Value)
        if NumberOfByte == 1:
            HexValue = hex(Value).split("x")[1].zfill(2)
            TempList = list()
            TempList.append(int("0x" + HexValue[0] + HexValue[1],16))
        if NumberOfByte == 2:
            HexValue = hex(Value).split("x")[1].zfill(4)
            TempList = list()
            TempList.append(int("0x" + HexValue[2] + HexValue[3],16))
            TempList.append(int("0x" + HexValue[0] + HexValue[1],16))
        Result = bytearray(TempList)
        return Result
    
    @staticmethod 
    def returnFloatToByte(Value,NumberOfByte):
        Value = float(Value)*float(100)
        Value = round(Value)
        if NumberOfByte == 1:
            HexValue = hex(Value).split("x")[1].zfill(2)
            TempList = list()
            TempList.append(int("0x" + HexValue[0] + HexValue[1],16))
        if NumberOfByte == 2:
            HexValue = hex(Value).split("x")[1].zfill(4)
            TempList = list()
            TempList.append(int("0x" + HexValue[2] + HexValue[3],16))
            TempList.append(int("0x" + HexValue[0] + HexValue[1],16))
        Result = bytearray(TempList)
        return Result
