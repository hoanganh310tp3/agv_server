from . import map_execution
from . import abc
from . import control_signal

class Population:
#     Mục đích: Khởi tạo một đối tượng Population với các giá trị mặc định hoặc dựa trên đầu vào của người dùng.
#     Cách hoạt động:
# Nếu Inbound và Outbound đều là 0, tức là không có điểm bắt đầu và kết thúc, đối tượng Population sẽ được khởi tạo với các thuộc tính:
# TravelledNode: Danh sách rỗng, tức là không có nút nào đã được đi qua.
# CostValue: Gán giá trị 100000, đại diện cho một chi phí rất lớn, có thể hiểu là không khả thi.
# ListOfControlSignal: Danh sách rỗng, không có tín hiệu điều khiển cho lộ trình.
# AbandonmentCounter: Bộ đếm từ bỏ, khởi tạo bằng 0.

    def __init__(self, Inbound=0, Outbound=0, LoadWeight=0, TimeStart=0, ignore_scheduling=False):
        if int(Inbound) == 0 and int(Outbound) == 0:
            self.TravelledNode = []
            self.CostValue = 100000
            self.ListOfControlSignal = []
            self.AbandonmentCounter = 0
            return
    
        self.TravelledNode = map_execution.Map.returnFeasiblePath(Inbound, Outbound)
        #NEW CODE WITHOUT SCHEDULING
        if not ignore_scheduling:
            if len(self.TravelledNode) >= 1 and self.TravelledNode[-1] == int(Outbound):
                self.ListOfControlSignal = control_signal.ControlSignal.returnListOfControlSignal(TimeStart, self.TravelledNode)
                self.CostValue = abc.ABC.returnCostFunction(self.ListOfControlSignal, Outbound, LoadWeight)
                self.AbandonmentCounter = 0
            else:
                self.CostValue = 100000
                self.ListOfControlSignal = []
                self.AbandonmentCounter = 0
        else:
            if self.TravelledNode and self.TravelledNode[-1] == int(Outbound):
                from . import road
                self.ListOfControlSignal = [control_signal.ControlSignal(road.Road(self.TravelledNode[i], self.TravelledNode[i+1])) for i in range(len(self.TravelledNode)-1)]
                self.CostValue = sum(cs.Road.Distance for cs in self.ListOfControlSignal)
            else:
                self.CostValue = 100000
                self.ListOfControlSignal = []
            self.AbandonmentCounter = 0
        # Nếu có giá trị Inbound và Outbound, phương thức sẽ tính toán tuyến đường khả thi từ Inbound đến Outbound.
#   Mục đích: Tính toán lộ trình và chi phí khi có đầu vào là Inbound và Outbound.
#   Cách hoạt động:
#   1.Tìm đường đi:
# Sử dụng phương thức map_execution.Map.returnFeasiblePath(Inbound, Outbound) để tìm tuyến đường khả thi từ điểm Inbound đến điểm Outbound.
# Danh sách các nút đã đi qua được lưu trong self.TravelledNode.
#   2.Kiểm tra tính hợp lệ:
# Nếu có ít nhất một nút trong danh sách TravelledNode, và điểm cuối của danh sách bằng với Outbound, tức là đã tìm được đường đi hợp lệ.
#   3.Tạo danh sách tín hiệu điều khiển:
# Nếu đường đi hợp lệ, gọi phương thức control_signal.ControlSignal.returnListOfControlSignal(TimeStart, self.TravelledNode) để tạo danh sách các tín hiệu điều khiển cho lộ trình này.
#   4.Tính chi phí:
# Tính toán chi phí của lộ trình bằng cách gọi abc.ABC.returnCostFunction(self.ListOfControlSignal, Outbound, LoadWeigth), sử dụng tín hiệu điều khiển, điểm đích và tải trọng để xác định.
# Gán chi phí cho thuộc tính self.CostValue.
# Đặt AbandonmentCounter bằng 0 (không có lần từ bỏ).
#   5.Xử lý nếu không tìm được lộ trình hợp lệ:
# Nếu không tìm được đường đi hợp lệ (điểm cuối của TravelledNode không phải là Outbound), chương trình sẽ gán chi phí CostValue bằng 100000 và danh sách tín hiệu điều khiển bằng rỗng. Điều này có nghĩa là lộ trình này không khả thi.
      
  
    #OLD CODE USING SCHEDULING
        # self.TravelledNode = map_execution.Map.returnFeasiblePath(Inbound,Outbound)
        # if (len(self.TravelledNode) >= 1):
        #     if(self.TravelledNode[len(self.TravelledNode) - 1] == int(Outbound)):
        #         self.ListOfControlSignal = control_signal.ControlSignal.returnListOfControlSignal(TimeStart,self.TravelledNode)
        #         self.CostValue = abc.ABC.returnCostFunction(self.ListOfControlSignal,Outbound,LoadWeigth)
        #         self.AbandonmentCounter = int(0)
        #         return
        # self.CostValue = float(100000)
        # self.ListOfControlSignal = list()
        # self.AbandonmentCounter = int(0)
        
    
        
        
# Population là một lớp định nghĩa các thuộc tính và phương thức để quản lý các thông tin liên quan đến một quần thể của AGV, tính toán tín hiệu điều khiển cho lộ trình đó và chi phí năng lượng tương ứng.
# Các thuộc tính:
# TravelledNode: Một danh sách các nút đã đi qua.
# CostValue: Giá trị chi phí của tuyến đường.
# ListOfControlSignal: Một danh sách các tín hiệu điều khiển.
# AbandonmentCounter: Số lần bỏ qua tuyến đường.
# Các phương thức:
# __init__: Phương thức khởi tạo, được sử dụng để khởi tạo các thuộc tính của lớp.
# Nếu Inbound và Outbound đều là 0, các thuộc tính sẽ được khởi tạo với giá trị mặc định.
# Nếu có giá trị Inbound và Outbound, phương thức sẽ tính toán tuyến đường khả thi từ Inbound đến Outbound.
# Nếu tuyến đường khả thi từ Inbound đến Outbound tồn tại, phương thức sẽ tính toán giá trị chi phí và tín hiệu điều khiển.
# Nếu không tìm được đường đi hợp lệ, chi phí được đặt là 100000, tức là không khả thi.

