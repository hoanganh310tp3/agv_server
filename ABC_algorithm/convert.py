from datetime import datetime

class Convert:  
    @staticmethod
#     Mục đích: Chuyển đổi thời gian ở định dạng "HH:MM:SS" thành dấu thời gian (timestamp).
#     Cách hoạt động:
# Phân tách chuỗi thời gian theo dấu hai chấm (":").
# Tạo đối tượng datetime sử dụng năm, tháng, và ngày hiện tại cùng với giờ, phút, giây từ chuỗi Time.
# Trả về giá trị timestamp tương ứng với thời gian đó.
    def TimeToTimeStamp(Time):
        Temp = Time.split(":")
        Date = datetime(datetime.now().year,datetime.now().month,datetime.now().day,int(Temp[0]),int(Temp[1]),int(Temp[2]))
        return datetime.timestamp(Date)
    
    @staticmethod
# Mục đích: Đảm bảo rằng số thời gian (giờ, phút, giây) luôn có hai chữ số (thêm số 0 ở đầu nếu cần).
# Cách hoạt động: Nếu giá trị thời gian nhỏ hơn 10, thêm số 0 vào trước giá trị, ngược lại trả về chuỗi thời gian ban đầu.
    def returnCorrectFormTime(Time):
        if(int(Time)<10):
            return "0" + str(Time)
        return str(Time) 
    
    @staticmethod 
#     Mục đích: Tính toán tổng thời gian di chuyển dựa trên danh sách các tín hiệu điều khiển.
#     Cách hoạt động:
# Lặp qua danh sách các tín hiệu điều khiển (ListOfControlSignal).
# Tính thời gian di chuyển cho từng đoạn đường bằng cách lấy khoảng cách chia cho vận tốc.
# Cộng dồn vào tổng thời gian di chuyển và trả về kết quả.   
    def returnScheduleToTravellingTime(ListOfControlSignal):
        TravellingTime = float(0)
        for EachControlSignal in ListOfControlSignal:
            TravellingTime = TravellingTime + float(EachControlSignal.Road.Distance)/float(EachControlSignal.Velocity)
        return TravellingTime
    
    @staticmethod 
#     Mục đích: Chuyển dấu thời gian (timestamp) thành chuỗi thời gian định dạng "HH:MM:SS".
#     Cách hoạt động:
# Chuyển timestamp thành đối tượng datetime.
# Sử dụng phương thức returnCorrectFormTime để đảm bảo giờ, phút, giây có hai chữ số và trả về chuỗi thời gian dạng "HH:MM:SS".
    def returnTimeStampToTime(TimeStamp):
        Time = datetime.fromtimestamp(TimeStamp)
        CorrectTime = Convert.returnCorrectFormTime(Time.hour) + ":" + Convert.returnCorrectFormTime(Time.minute) + ":" + Convert.returnCorrectFormTime(Time.second)
        return CorrectTime
    
    @staticmethod 
#     Mục đích: Chuyển một giá trị số nguyên thành mảng byte với số byte cụ thể (1 hoặc 2 byte).
#     Cách hoạt động:
# Chuyển giá trị số nguyên thành hệ thập lục phân (hex).
# Tách chuỗi hex và thêm các giá trị byte tương ứng vào một danh sách TempList.
# Kết quả là một bytearray chứa các byte biểu diễn giá trị số nguyên.
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
#     Mục đích: Chuyển giá trị số thực thành mảng byte với số byte cụ thể.
#     Cách hoạt động:
# Nhân giá trị số thực với 100 và làm tròn giá trị.
# Tương tự như phương thức returnIntToByte, chuyển đổi số thành dạng hex và tách các byte tương ứng.
# Trả về kết quả dưới dạng bytearray.
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
    
# Convert cung cấp các hàm tiện ích để chuyển đổi thời gian, dấu thời gian, và giá trị số sang dạng byte.
# Nó xử lý cả số nguyên và số thực, đảm bảo tính chính xác và dễ dàng sử dụng trong các ứng dụng cần truyền dữ liệu dưới dạng byte hoặc tính toán thời gian.





