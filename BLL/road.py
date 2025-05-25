import DTO.map_topology
import DTO.road
import BLL.road
import DTO.agv_car          

class Road:
    @staticmethod
    def GetDistance(PreviousNode, NextNode):
        return float(DTO.map_topology.MapTopology.Map[int(PreviousNode)][int(NextNode)])
    
    def GetDirection(PreviousNode, NextNode):
        return int(DTO.map_topology.MapTopology.Direction[int(PreviousNode)][int(NextNode)])
    
# hướng đông = 2
# hướng tây = 4
# hướng nam = 3
# hướng bắc = 1
# vô hướng = 5
    
# Số 1: Đi thẳng 
# Số 2: Rẽ phải
# Số 3: Rẽ trái
# Số 4: Quay đầu
# Số 0: không cần xử lý hướng


    @staticmethod
    def returnListOfRoad(ListOfNode):
        ListOfRoad = list()
        for i in range(0, len(ListOfNode)-1):
            UnProcessedDirection1 = BLL.road.Road.GetDirection(ListOfNode[i], ListOfNode[i+1])
            
            # For the last road segment, maintain the previous ProcessedDirection
            if i == len(ListOfNode)-2:
                # Skip direction processing for last segment
                ProcessedDirection = 0
            else:
                UnProcessedDirection2 = BLL.road.Road.GetDirection(ListOfNode[i+1], ListOfNode[i+2])
            
            # Process directions only for non-last segments
            if UnProcessedDirection2 == UnProcessedDirection1:
                ProcessedDirection = 1
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 4:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 3:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 2 and UnProcessedDirection2 == 1:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 2:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 3:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 4 and UnProcessedDirection2 == 1:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 2:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 4:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 3 and UnProcessedDirection2 == 1:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 2:
                ProcessedDirection = 2
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 4:
                ProcessedDirection = 3
            elif UnProcessedDirection1 == 1 and UnProcessedDirection2 == 3:
                ProcessedDirection = 4
            elif UnProcessedDirection1 == 5 or UnProcessedDirection2 == 5:
                ProcessedDirection = 0
            else:
                pass
            Road = DTO.road.Road(ListOfNode[i],ListOfNode[i+1],BLL.road.Road.GetDistance(ListOfNode[i],ListOfNode[i+1]), ProcessedDirection)
            ListOfRoad.append(Road)
        return ListOfRoad
    
    
    
    @staticmethod
    def find_shared_points(list_of_routes):
        """
        Input: list_of_routes là list chứa các ListOfRoad của các xe
        Return: Tuple (CP, SCP) trong đó:
            - CP: dictionary với key là index của route, value là list các điểm chung
            - SCP: dictionary với key là index của route, value là list các tập điểm chung liền kề
        """
        # Khởi tạo dictionaries để lưu kết quả
        CP = {}  # Common Points
        SCP = {} # Sequential Common Points
        
        # Tạo list các nodes cho mỗi route bằng cách trích xuất TravelledNode
        route_nodes = []
        for route in list_of_routes:
            # Xây dựng lại TravelledNode từ các Road segments
            nodes = []
            if not route:
                route_nodes.append(nodes)
                continue
            
            # Thêm điểm đầu tiên của đoạn đường đầu tiên
            nodes.append(route[0].FirstNode)
            
            # Thêm tất cả các điểm cuối của từng đoạn đường
            for road in route:
                nodes.append(road.SecondNode)
            
            route_nodes.append(nodes)
        
        # Tìm điểm chung (CP) cho mỗi route
        for i in range(len(route_nodes)):
            CP[i] = []
            current_route = route_nodes[i]
            
            # So sánh với tất cả các route khác
            for j in range(len(route_nodes)):
                if i != j:
                    other_route = route_nodes[j]
                    for node in current_route:
                        if node in other_route and node not in CP[i]:
                            CP[i].append(node)
            
            # Sắp xếp CP theo thứ tự xuất hiện trong route gốc
            CP[i] = sorted(CP[i], key=lambda x: current_route.index(x))
        
        # Tìm các tập điểm chung liền kề (SCP)
        for i in range(len(route_nodes)):
            SCP[i] = []
            current_cp = CP[i]
            current_route = route_nodes[i]
            
            if len(current_cp) < 2:
                continue
            
            # Tìm các chuỗi điểm liền kề
            temp_sequence = [current_cp[0]]
            for k in range(1, len(current_cp)):
                current_idx = current_route.index(current_cp[k])
                prev_idx = current_route.index(current_cp[k-1])
                
                # Kiểm tra xem hai điểm có liền kề trong route gốc không
                if current_idx - prev_idx == 1:
                    temp_sequence.append(current_cp[k])
                else:
                    if len(temp_sequence) >= 2:
                        SCP[i].extend(temp_sequence)
                    temp_sequence = [current_cp[k]]
            
            # Xử lý chuỗi cuối cùng
            if len(temp_sequence) >= 2:
                SCP[i].extend(temp_sequence)
        
        return CP, SCP

    @staticmethod
    def allocate_spare_points(route_index, list_of_routes):
        """
        Phân bổ spare points cho một route cụ thể theo thuật toán 4.
        
        Input:
            - route_index: index của route cần phân bổ spare point
            - list_of_routes: list chứa các ListOfRoad của các xe
        
        Return:
            - SP: List các spare points được phân bổ
        """
        # Bước 1: Tìm CP và SCP
        CP, SCP = BLL.road.Road.find_shared_points(list_of_routes)
        
        # Lấy SCP của route hiện tại
        if route_index not in SCP or not SCP[route_index]:
            return []
        
        current_scp = SCP[route_index]
        
        # Bước 2: Tìm tất cả free points
        # Tạo list các nodes cho mỗi route
        route_nodes = []
        for route in list_of_routes:
            nodes = []
            if not route:
                route_nodes.append(nodes)
                continue
                
            # Thêm điểm đầu tiên của đoạn đường đầu tiên
            if route:
                nodes.append(route[0].FirstNode)
            
            # Thêm tất cả các điểm cuối của từng đoạn đường
            for road in route:
                nodes.append(road.SecondNode)
                
            route_nodes.append(nodes)
        
        # Tìm tất cả các node đã được sử dụng
        occupied_nodes = set()
        for route in route_nodes:
            for node in route:
                if node and node != "":
                    occupied_nodes.add(int(node))
        
        # Tìm free points - sử dụng số lượng node từ ma trận bản đồ
        map_size = len(DTO.map_topology.MapTopology.Map)
        all_nodes = set(range(map_size))
        free_points = all_nodes - occupied_nodes
        
        # Bước 3: Phân bổ spare points theo thuật toán 4
        SP = []  # List chứa các spare points được phân bổ
        
        for node in current_scp:
            if node and node != "":
                node_int = int(node)
                
                # Tìm các free points kề với node
                connected_fp = []
                for fp in free_points:
                    distance = BLL.road.Road.GetDistance(node_int, fp)
                    if distance < 100000 and distance > 0:
                        connected_fp.append((fp, distance))
                
                # Nếu có free points kề
                if connected_fp:
                    # Sắp xếp theo khoảng cách
                    connected_fp.sort(key=lambda x: x[1])
                    # Chọn điểm gần nhất
                    nearest_fp = connected_fp[0][0]
                    SP.append(nearest_fp)
                else:
                    # Nếu không có free points kề, trả về rỗng theo thuật toán
                    return []
        
        return SP