import DTO.requirement
import BLL.schedule
import DTO.schedule
import BLL.abc
import datetime
from requests_management.models import order_data
# Đoạn mã này định nghĩa lớp Requirement để quản lý các yêu cầu vận chuyển hàng hóa bằng xe AGV. Nó cũng bao gồm một phương thức tĩnh để đọc dữ liệu từ bảng cơ sở dữ liệu (hoặc tệp CSV trong mã bị chú thích) và tạo danh sách các yêu cầu vận chuyển.
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

class Requirement:
    @staticmethod
    def ReadTimeTable():
        try:
            orderQuerySet = order_data.objects.all().order_by('start_time')
            
            if not orderQuerySet.exists():
                print("No orders found")
                return []
                
            listOfOrders = []
            
            for eachOrder in orderQuerySet:
                try:
                    requirement = DTO.requirement.Requirement()
                    requirement.Order = int(eachOrder.order_number)
                    requirement.Date = str(eachOrder.order_date)
                    requirement.Name = str(eachOrder.load_name)
                    requirement.Number = int(eachOrder.load_amount)
                    requirement.LoadWeight = float(eachOrder.load_weight)
                    requirement.TimeStart = str(eachOrder.start_time)
                    requirement.Inbound = int(eachOrder.start_point)
                    requirement.Outbound = int(eachOrder.end_point)
                    listOfOrders.append(requirement)
                    
                except Exception as e:
                    print(f"Error processing order {eachOrder.order_id}: {e}")
                    continue
                    
            return listOfOrders
            
        except Exception as e:
            print(f"Error reading time table: {e}")
            return []