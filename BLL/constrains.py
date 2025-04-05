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
        Kiểm tra và xử lý va chạm với logic DSPA (Dynamic Shared Point Allocation)
        Input:
            TimeStart: Thời điểm bắt đầu
            Road: Đoạn đường đang xét
            ResidualPath: Đường đi còn lại của xe (optional)
        Return:
            ControlSignal: Tín hiệu điều khiển cho xe với thêm thuộc tính waitTime
        """
        ControlSignal = DTO.control_signal.ControlSignal(Road)
        # Thêm thuộc tính waitTime
        ControlSignal.waitTime = 0
        
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
        
        # Danh sách các điểm reserved bởi xe khác
        reserved_points = [p.SecondNode for p in other_positions]
        
        # Điều kiện 1: SecondNode không thuộc SCP và không bị reserved bởi xe khác
        if not in_scp and current_state.secondNode not in reserved_points:
            current_state.SA = 1  # Xe di chuyển bình thường
            current_state.F = 0   # Không đi vào SCP
            return ControlSignal
        
        # Điều kiện 2: SecondNode thuộc SCP và không có điểm nào trong SCP bị reserved 
        # bởi xe khác với F=0
        if in_scp:
            scp_is_free = True
            for node in SCP[route_index]:
                for pos in other_positions:
                    # Kiểm tra nếu node này là reserved point của xe khác
                    if node == pos.SecondNode:
                        # Lấy F của xe khác
                        other_schedule = next((s for s in DTO.schedule.Schedule.ListOfSchedule 
                                            if s.Car == pos.Car), None)
                        other_F = 0
                        if hasattr(other_schedule, 'F'):
                            other_F = other_schedule.F
                        
                        # Nếu xe khác có F=0, SCP không trống
                        if other_F == 0:
                            scp_is_free = False
                            break
        
            # Nếu SCP trống hoặc chỉ có xe với F=1, xe có thể đi
            if scp_is_free and current_state.secondNode not in reserved_points:
                current_state.SA = 1
                current_state.F = 1  # Đang đi vào SCP
                return ControlSignal
        
        # Điều kiện 3: SecondNode thuộc SCP và có điểm trong SCP bị reserved, nhưng
        # xe khác chưa đi vào SCP (F=0) và có spare points
        if in_scp:
            # Tìm spare points
            spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
            
            # Kiểm tra xem có điểm nào trong SCP bị reserved bởi xe khác với F=0 không
            other_car_reserved_scp = False
            for node in SCP[route_index]:
                for pos in other_positions:
                    if node == pos.SecondNode:
                        other_schedule = next((s for s in DTO.schedule.Schedule.ListOfSchedule 
                                            if s.Car == pos.Car), None)
                        other_F = 0
                        if hasattr(other_schedule, 'F'):
                            other_F = other_schedule.F
                        
                        if other_F == 0:
                            other_car_reserved_scp = True
                            break
            
            # Nếu có spare points và SecondNode không bị reserved
            if spare_points and other_car_reserved_scp and current_state.secondNode not in reserved_points:
                current_state.SP = spare_points
                current_state.SA = 1
                current_state.F = 1
                
                # Nếu xe đã đi vào SCP (F=1) và firstNode là spare point, xóa nó khỏi SP
                if current_state.firstNode in spare_points:
                    current_state.SP.remove(current_state.firstNode)
                
                return ControlSignal
        
        # Xử lý deadlock
        # Kiểm tra Heading-on deadlock
        for pos in other_positions:
            # Heading-on deadlock: SecondNode của xe này là FirstNode của xe khác và ngược lại
            if current_state.secondNode == pos.FirstNode and pos.SecondNode == current_state.firstNode:
                # Nếu xe hiện tại có F=1 (đã đi vào SCP), sử dụng spare point
                if current_state.F == 1:
                    spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
                    if spare_points:
                        nearest_spare = spare_points[0]
                        # Di chuyển tới spare point
                        ControlSignal.Road = DTO.road.Road(
                            current_state.firstNode,
                            nearest_spare,
                            BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                            0
                        )
                        # Thêm thuộc tính waitTime
                        ControlSignal.waitTime = 0
                        return ControlSignal
                else:
                    # Xe khác sẽ di chuyển - hiện tại đợi tại chỗ
                    current_state.SA = 2  # Waiting
                    # Sử dụng cách dừng xe từ thuật toán cũ
                    ControlSignal.Road = DTO.road.Road(0, 0, 100000)
                    ControlSignal.waitTime = 5  # Thời gian đợi mặc định 5s
                    return ControlSignal
        
        # Kiểm tra Loop deadlock
        is_loop_deadlock = Constrains._check_loop_deadlock(TimeStart, current_state, other_positions)
        if is_loop_deadlock:
            spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
            if spare_points and current_state.F == 1:
                # Di chuyển tới spare point
                nearest_spare = spare_points[0]
                ControlSignal.Road = DTO.road.Road(
                    current_state.firstNode,
                    nearest_spare,
                    BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                    0
                )
                ControlSignal.waitTime = 0
                return ControlSignal
            else:
                # Đợi tại chỗ
                current_state.SA = 2
                # Sử dụng cách dừng xe từ thuật toán cũ
                ControlSignal.Road = DTO.road.Road(0, 0, 100000)
                ControlSignal.waitTime = 5  # Thời gian đợi mặc định
                return ControlSignal
        
        # Nếu không thỏa mãn điều kiện nào - đợi tại chỗ
        current_state.SA = 2
        # Sử dụng cách dừng xe từ thuật toán cũ
        ControlSignal.Road = DTO.road.Road(0, 0, 100000)
        ControlSignal.waitTime = 0
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
            if pos.FirstNode and pos.SecondNode:
                next_moves[pos.FirstNode] = pos.SecondNode
        
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