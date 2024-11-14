from . import abc
from . import schedule

# import sẽ bị comment out nếu ta dùng file csv để test
from requests_management.models import order_data
# Đoạn mã này định nghĩa lớp Requirement để quản lý các yêu cầu vận chuyển hàng hóa bằng xe AGV. Nó cũng bao gồm một phương thức tĩnh để đọc dữ liệu từ bảng cơ sở dữ liệu (hoặc tệp CSV trong mã bị chú thích) và tạo danh sách các yêu cầu vận chuyển.
class Requirement:
    # Định nghĩa lớp Requirement với các thuộc tính và phương thức khởi tạo.
# Order: Số đơn hàng.
# Name: Tên hàng hóa.
# CalledCar: Xe được gọi để thực hiện đơn hàng.
# Date: Ngày thực hiện đơn hàng.
# LoadWeight: Trọng lượng của hàng hóa.
# TimeStart: Thời gian bắt đầu vận chuyển.
# Inbound: Nút (node) nơi hàng hóa được lấy.
# Outbound: Nút (node) nơi hàng hóa được giao.
# Number: Số lượng hàng hóa.
    def __init__(self, Order="", Name="", Number="", Weight="", TimeStart="", Inbound="", Outbound="", CalledCar="", Date=""):
        self.Order = Order
        self.Name = Name
        self.CalledCar = CalledCar
        self.Date = Date
        self.LoadWeight = Weight
        self.TimeStart = TimeStart
        self.Inbound = Inbound
        self.Outbound = Outbound
        self.Number = Number
    # Phương thức __str__ để trả về một chuỗi biểu diễn các thuộc tính của đối tượng.
    def __str__(self):
        return f"{self.Order}, {self.Date}, {self.Name}, {self.CalledCar}, {self.Inbound}, {self.Outbound}"

    @staticmethod
#     Chức năng:
# Phương thức ReadTimeTable lấy toàn bộ dữ liệu từ bảng order_data trong cơ sở dữ liệu, sắp xếp theo thời gian bắt đầu và chuyển đổi từng hàng dữ liệu thành một đối tượng Requirement.
#     Giải thích chi tiết:
#     orderQuerySet = order_data.objects.all().order_by('start_time'): Lấy tất cả dữ liệu từ bảng order_data và sắp xếp theo cột start_time (thời gian bắt đầu).
#     listOfOrders = list(): Tạo danh sách rỗng để lưu trữ các đối tượng Requirement.
#     Vòng lặp qua từng đơn hàng:
# for eachOrder in orderQuerySet:: Lặp qua từng dòng dữ liệu trong bảng.
# Tạo một đối tượng Requirement mới cho mỗi dòng và gán các thuộc tính tương ứng từ các trường trong bảng.
# requirement.Order, requirement.Date, requirement.Name, ...: Gán các giá trị tương ứng cho các thuộc tính của đối tượng Requirement.
#      listOfOrders.append(requirement): Thêm đối tượng Requirement đã được tạo vào danh sách.
#      return listOfOrders: Trả về danh sách các yêu cầu.

    def ReadTimeTable():
        orderQuerySet = order_data.objects.all().order_by('start_time')
        
        listOfOrders = list()
        
        for eachOrder in orderQuerySet:
            requirement = Requirement()
            requirement.Order = int(eachOrder.order_id)
            requirement.Date = str(eachOrder.order_date)
            requirement.Name = str(eachOrder.load_name)
            requirement.Number = int(eachOrder.load_amount)
            requirement.LoadWeight = float(eachOrder.load_weight)
            requirement.TimeStart = str(eachOrder.start_time)
            requirement.Inbound = int(eachOrder.start_point)
            requirement.Outbound = int(eachOrder.end_point)
            listOfOrders.append(requirement)
            
        return listOfOrders

#test bằng file csv
# Mã bị chú thích này là phiên bản đọc dữ liệu từ tệp CSV thay vì từ cơ sở dữ liệu.
# open("TimeTable.csv",'r'): Mở tệp CSV chứa thông tin đơn hàng.
# for line in f:: Đọc từng dòng của tệp và chia tách các giá trị để gán vào đối tượng Requirement.
    # def ReadTimeTable():
    #     f = open("TimeTable.csv",'r')
    #     temp = f.readline()
    #     ListOfRequirement = list()
    #     for line in f:
    #         temp = line.strip().split(',')
    #         requirement = Requirement()
    #         requirement.Order = int(temp[0])
    #         requirement.Name = str(temp[1])
    #         requirement.Number = int(temp[2])
    #         requirement.LoadWeight = float(temp[3])
    #         requirement.TimeStart = str(temp[4])
    #         requirement.Inbound = int(temp[5])
    #         requirement.Outbound = int(temp[6])
    #         ListOfRequirement.append(requirement)
    #     f.close()

    #     return ListOfRequirement
    
# Lớp Requirement được sử dụng để lưu trữ và quản lý thông tin về các đơn hàng.
# Phương thức tĩnh ReadTimeTable đọc dữ liệu từ cơ sở dữ liệu (hoặc từ tệp CSV) và trả về danh sách các yêu cầu vận chuyển.