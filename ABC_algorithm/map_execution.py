import numpy
import os
from . import abc_parameters
import environ
# Xử lý bản đồ và các yếu tố liên quan đến đường đi.
# Đoạn mã này định nghĩa lớp Map với các phương thức nhằm mục đích tạo ra bản đồ, tính toán các yếu tố khả thi của đường đi và tìm ra tuyến đường khả thi dựa trên đầu vào. 
env = environ.Env()
environ.Env.read_env()

class Map:
    @staticmethod
#     Mục đích: Tính toán ma trận hệ số khả thi của đường đi giữa các nút trên bản đồ dựa trên danh sách các đường đi được cung cấp.
#     Cách hoạt động:
# RoadList là ma trận các đường đi, với giá trị 100000 đại diện cho đường không thể đi qua và 0 đại diện cho điểm trùng khớp (tự nối).
# FeasibleFactor lưu trữ tỷ lệ khả thi cho mỗi tuyến đường có thể đi từ một nút đến các nút khác.
#     Đối với mỗi hàng trong ma trận đường đi:
# Đếm số đường có thể đi từ nút đó.
# Xác định hệ số khả thi cho mỗi đường bằng cách chia 100 cho số lượng đường khả thi và cập nhật vào ma trận FeasibleFactor.
# Trả về ma trận hệ số khả thi.
    def returnFeasiblePathFactor(RoadList):
        Length = len(RoadList)
        FeasibleFactor = numpy.empty((Length, Length)) 
        for i in range(Length):
            Count = float(0)
            for j in range(Length):
                if(float(RoadList[i][j]) != 100000 and float(RoadList[i][j]) != 0):
                    Count = Count +1   
            for j in range(Length):
                if(float(RoadList[i][j]) != 100000 and float(RoadList[i][j]) != 0):
                    FeasibleFactor[i][j] = 100/float(Count)
                else:
                    FeasibleFactor[i][j] = 0
        return FeasibleFactor
    


    @staticmethod
#    Mục đích: Đọc dữ liệu từ file CSV và trả về thông tin về các nút và hướng của đường đi.
#    Cách hoạt động:
# Mở và đọc file Map3_test.csv, lưu trữ dữ liệu vào danh sách RoadList.
# Tạo hai danh sách NodeList và DirectionList, chứa lần lượt các nút và hướng của đường đi.
# Mỗi phần tử trong RoadList được tách thành hai phần: nút và hướng của nút (tách bằng dấu ;).
# Trả về một tuple chứa danh sách các nút và danh sách các hướng.
    def returnMap():
        # Đi lên một cấp thư mục để tìm thư mục web_management
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, 'Map3.csv')
        
        try:
            with open(file_path, 'r') as f:
                RoadList = [line.strip().split(',') for line in f]
        except FileNotFoundError:
            print(f"Warning: The file 'Map3.csv' was not found in {current_dir}. Using a default map.")
            RoadList = [
                ["0;N", "1;E", "100000;", "100000;"],
                ["1;W", "0;S", "2;E", "100000;"],
                ["100000;", "2;W", "0;S", "3;E"],
                ["100000;", "100000;", "3;W", "0;N"]
            ]
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}. Using a default map.")
            RoadList = [
                ["0;N", "1;E", "100000;", "100000;"],
                ["1;W", "0;S", "2;E", "100000;"],
                ["100000;", "2;W", "0;S", "3;E"],
                ["100000;", "100000;", "3;W", "0;N"]
            ]

        NodeList = []
        DirectionList = []

        for eachLine in RoadList:
            NodeLine = []
            DirectionLine = []
            for eachNode in eachLine:
                node_parts = eachNode.split(';')
                if len(node_parts) > 1:
                    NodeLine.append(node_parts[0])
                    DirectionLine.append(node_parts[1])
                else:
                    NodeLine.append(node_parts[0])
                    DirectionLine.append('')  # or some default value
            NodeList.append(NodeLine)
            DirectionList.append(DirectionLine)
        
        # Convert NodeList to integers
        NodeList = [[int(node) if node.isdigit() else 100000 for node in row] for row in NodeList]
        
        return (NodeList, DirectionList)


    
# finding feasible path
    @staticmethod
#     Mục đích: Tìm tuyến đường khả thi từ nút Inbound đến Outbound.
#     Cách hoạt động:
# Gọi phương thức returnMap() để lấy ma trận đường đi và phương thức returnFeasiblePathFactor() để lấy ma trận hệ số khả thi.
# Bắt đầu từ nút Inbound, lưu các nút đã đi qua vào danh sách TravelledNode.
# Sử dụng số ngẫu nhiên (RandomNumber) và hệ số khả thi để chọn tuyến đường tiếp theo từ nút hiện tại (CurrentNode).
# Cập nhật hệ số khả thi để tránh đi lại các nút đã đi qua.
# Nếu vượt quá số lần thử nghiệm tối đa (nCount), trả về danh sách các nút đã đi qua.
# Tiếp tục lặp cho đến khi đến được nút Outbound hoặc không tìm được đường đi khả thi nào.
    def returnFeasiblePath(Inbound, Outbound):
        RoadList = Map.returnMap()[0]
        FeasibleFactor = Map.returnFeasiblePathFactor(RoadList)
        Count = int(0)
        TravelledNode = list()
        TravelledNode.append(int(Inbound))
        CurrentNode = int(Inbound)
        HighPoint = float(100)
        while (CurrentNode != int(Outbound)):
            Count = Count + 1
            if(Count == abc_parameters.ABCSetting.nCount):  # Thay thế bằng ABCSetting.nCount nếu cần
                return TravelledNode
            Flag = bool(False)
            RandomNumber = numpy.random.uniform(1,HighPoint)
            Probability = FeasibleFactor[CurrentNode][0]
            for j in range (0,len(RoadList)):
                if(RandomNumber < Probability):
                    CurrentNode = j
                    TravelledNode.append(int(j))
                    Flag = True
                    HighPoint = 100
                    for Element in TravelledNode:
                        FeasibleFactor[j][Element] = 0
                    break
                else:
                    if(int(j) < len(RoadList) -1 ):
                        Probability  = Probability + FeasibleFactor[CurrentNode][j+1]
            if(Flag == False):
                HighPoint = RandomNumber
                continue
        return TravelledNode
# end finding feasible path

# Map cung cấp các phương thức để đọc dữ liệu bản đồ, tính toán hệ số khả thi cho các tuyến đường, và tìm tuyến đường từ nút Inbound đến Outbound dựa trên xác suất và số ngẫu nhiên.
# Nó có thể được sử dụng trong các hệ thống điều khiển AGV để tìm tuyến đường khả thi trên bản đồ.