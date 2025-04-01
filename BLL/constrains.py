import DTO.schedule
import DTO.road
import BLL.position
import DTO.agv_car
import DTO.control_signal
import BLL.road
import BLL.convert

class Constrains:
    class AGVState:
        def __init__(self):
            self.SA = 2  # 2: waiting, 1: normal operation
            self.F = 0   # 1: moving in SCP, 0: not in SCP
            self.firstNode = None  # Last point AGV left
            self.secondNode = None # Next point to visit
            self.reservedPoint = None # Reserved point
            self.SP = []  # Spare points
            self.residualPath = []  # Đường đi còn lại

    @staticmethod
    def CollisionConstrain(TimeStart, Road, ResidualPath=None):
        """
        Kiểm tra và xử lý va chạm với logic mới sử dụng dynamic shared point
        Input:
            TimeStart: Thời điểm bắt đầu
            Road: Đoạn đường đang xét
            ResidualPath: Đường đi còn lại của xe (optional)
        Return:
            ControlSignal: Tín hiệu điều khiển cho xe
        """
        Test = BLL.convert.Convert.returnTimeStampToTime(TimeStart)
        ControlSignal = DTO.control_signal.ControlSignal(Road)
        
        # Khởi tạo trạng thái hiện tại của xe
        current_state = Constrains.AGVState()
        current_state.firstNode = Road.FirstNode
        current_state.secondNode = Road.SecondNode
        current_state.reservedPoint = Road.SecondNode  # Mặc định dự định đi đến secondNode
        
        if ResidualPath:
            current_state.residualPath = ResidualPath
        
        # Nếu không có lịch trình nào khác, xe di chuyển bình thường
        if len(DTO.schedule.Schedule.ListOfSchedule) == 0:
            current_state.SA = 1
            return ControlSignal

        # Lấy danh sách routes và vị trí hiện tại của tất cả xe
        list_of_routes = []
        other_positions = []
        for schedule in DTO.schedule.Schedule.ListOfSchedule:
            route = []
            for signal in schedule.ListOfControlSignal:
                route.append(signal.Road)
            list_of_routes.append(route)
            
            # Lấy vị trí hiện tại của xe
            pos = BLL.position.Position.returnPosition(TimeStart, schedule)
            if pos.FirstNode:  # Chỉ xem xét các xe đang hoạt động
                other_positions.append(pos)

        # Tìm CP và SCP cho tất cả routes
        CP, SCP = BLL.road.Road.find_shared_points(list_of_routes)
        route_index = list_of_routes.index(Road) if Road in list_of_routes else -1
        
        # Kiểm tra xem secondNode có thuộc SCP không
        in_scp = False
        if route_index != -1 and route_index in SCP:
            in_scp = current_state.secondNode in SCP[route_index]
        
        # Condition 1: Điểm tiếp theo không bị chiếm bởi xe khác
        second_node_is_free = current_state.secondNode not in [p.reservedPoint for p in other_positions]
        
        if second_node_is_free:
            if not in_scp:
                # Trường hợp bình thường - di chuyển không vào SCP
                current_state.SA = 1
                current_state.F = 0
                return ControlSignal
            else:
                # Condition 2: Nếu secondNode thuộc SCP, kiểm tra tất cả các điểm trong SCP
                scp_is_free = True
                
                # Kiểm tra xem các điểm trong SCP có bị chiếm không
                for node in SCP[route_index]:
                    for pos in other_positions:
                        # Nếu điểm đã bị chiếm nhưng xe chiếm đang di chuyển trong SCP (F=1)
                        # thì vẫn có thể di chuyển
                        if (node == pos.firstNode or node == pos.reservedPoint):
                            other_schedule = next((s for s in DTO.schedule.Schedule.ListOfSchedule 
                                                if s.Car == pos.Car), None)
                            other_F = 0  # Giả định mặc định
                            
                            if hasattr(other_schedule, 'F'):
                                other_F = other_schedule.F
                                
                            if other_F != 1:
                                scp_is_free = False
                                break
                
                if scp_is_free:
                    # Trường hợp SCP trống hoặc chỉ có xe với F=1
                    current_state.SA = 1
                    current_state.F = 1
                    return ControlSignal
        
        # Condition 3: Áp dụng spare points
        spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
        if spare_points:
            current_state.SP = spare_points
            current_state.SA = 1
            current_state.F = 1
            
            # Nếu xe đã đi vào SCP (F=1), cập nhật spare point
            if current_state.F == 1 and current_state.firstNode in spare_points:
                current_state.SP.remove(current_state.firstNode)
            
            # Cập nhật đường đi - thêm spare point vào
            if current_state.residualPath:
                nearest_spare = spare_points[0]  # Lấy spare point đầu tiên
                # Tạo đường đi tạm thời để tránh deadlock
                ControlSignal.Road = DTO.road.Road(
                    current_state.firstNode,
                    nearest_spare,
                    BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                    0
                )
                return ControlSignal
        
        # Xử lý deadlock
        for pos in other_positions:
            # Heading-on deadlock
            if current_state.secondNode == pos.firstNode and pos.secondNode == current_state.firstNode:
                if current_state.F == 1:
                    # Xe hiện tại đi vào spare point
                    if spare_points:
                        nearest_spare = spare_points[0]
                        ControlSignal.Road = DTO.road.Road(
                            current_state.firstNode,
                            nearest_spare,
                            BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                            0
                        )
                        return ControlSignal
                else:
                    # Xe khác sẽ di chuyển tới spare point - giữ nguyên vị trí hiện tại
                    current_state.SA = 2  # Đợi
                    ControlSignal.Road = DTO.road.Road(
                        current_state.firstNode,
                        current_state.firstNode,  # Giữ nguyên vị trí
                        0,
                        0
                    )
                    return ControlSignal
            
            # Cross/Loop deadlock
            elif pos.secondNode == current_state.firstNode:
                # Kiểm tra loop deadlock
                is_deadlock = Constrains._check_loop_deadlock(TimeStart, current_state, other_positions)
                if is_deadlock:
                    if current_state.F == 1 and spare_points:
                        # Di chuyển tới spare point
                        nearest_spare = spare_points[0]
                        ControlSignal.Road = DTO.road.Road(
                            current_state.firstNode,
                            nearest_spare,
                            BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                            0
                        )
                        return ControlSignal
        
        # Nếu không thỏa mãn điều kiện nào - đợi tại chỗ
        current_state.SA = 2
        ControlSignal.Road = DTO.road.Road(
            current_state.firstNode,
            current_state.firstNode,
            0,
            0
        )
        return ControlSignal

    @staticmethod
    def _check_loop_deadlock(TimeStart, current_state, other_positions):
        """
        Kiểm tra xem có tồn tại loop deadlock không
        """
        visited = set()
        current = current_state.firstNode
        
        # Tạo dictionary ánh xạ từ firstNode đến secondNode
        next_moves = {}
        for pos in other_positions:
            if pos.firstNode and pos.secondNode:
                next_moves[pos.firstNode] = pos.secondNode
        
        # Thêm current_state vào
        next_moves[current_state.firstNode] = current_state.secondNode
        
        # Kiểm tra chu trình
        while current not in visited:
            visited.add(current)
            
            if current not in next_moves:
                return False
                
            current = next_moves[current]
            
            if current == current_state.firstNode:
                return True
        
        return False