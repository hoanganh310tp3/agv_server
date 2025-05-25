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
            self.residualPath = []  # Remaining path

    @staticmethod
    def CollisionConstrain(TimeStart, Road, ResidualPath=None):
        """
        Check and handle collisions using DSPA (Dynamic Shared Point Allocation) logic
        Input:
            TimeStart: Start time
            Road: Current road segment
            ResidualPath: Remaining path of the vehicle (optional)
        Return:
            ControlSignal: Control signal for the vehicle with additional waitTime attribute
        """
        ControlSignal = DTO.control_signal.ControlSignal(Road)
        # Add waitTime attribute
        ControlSignal.waitTime = 0
        
        # IMPORTANT: Update Action from Road.Direction
        ControlSignal.Action = Road.Direction
        
        # Initialize current state of the vehicle
        current_state = Constrains.AGVState()
        current_state.firstNode = Road.FirstNode
        current_state.secondNode = Road.SecondNode
        current_state.reservedPoint = Road.SecondNode  # Default plan is to go to secondNode
        
        if ResidualPath:
            current_state.residualPath = ResidualPath
        
        # If there are no other schedules, vehicle moves normally
        if len(DTO.schedule.Schedule.ListOfSchedule) == 0:
            current_state.SA = 1
            return ControlSignal

        # Get list of routes and current positions of all vehicles
        list_of_routes = []
        other_positions = []
        for schedule in DTO.schedule.Schedule.ListOfSchedule:
            route = []
            for signal in schedule.ListOfControlSignal:
                route.append(signal.Road)
            list_of_routes.append(route)
            
            # Get current position of the vehicle
            pos = BLL.position.Position.returnPosition(TimeStart, schedule)
            if pos.FirstNode:  # Only consider active vehicles
                other_positions.append(pos)

        # Find CP and SCP for all routes
        CP, SCP = BLL.road.Road.find_shared_points(list_of_routes)
        route_index = list_of_routes.index(Road) if Road in list_of_routes else -1
        
        # Check if secondNode belongs to SCP
        in_scp = False
        if route_index != -1 and route_index in SCP:
            in_scp = current_state.secondNode in SCP[route_index]
        
        # List of points reserved by other vehicles
        reserved_points = [p.SecondNode for p in other_positions]
        
        # Condition 1: SecondNode is not in SCP and not reserved by other vehicles
        if not in_scp and current_state.secondNode not in reserved_points:
            current_state.SA = 1
            current_state.F = 0   # Not entering SCP
            return ControlSignal
        
        # Condition 2: SecondNode is in SCP and no point in SCP is reserved
        # by other vehicles with F=0
        if in_scp:
            scp_is_free = True
            for node in SCP[route_index]:
                for pos in other_positions:
                    # Check if this node is a reserved point of another vehicle
                    if node == pos.SecondNode:
                        # Get F of the other vehicle
                        other_schedule = next((s for s in DTO.schedule.Schedule.ListOfSchedule 
                                            if s.Car == pos.Car), None)
                        other_F = 0
                        if hasattr(other_schedule, 'F'):
                            other_F = other_schedule.F
                        
                        # If other vehicle has F=0, SCP is not empty
                        if other_F == 0:
                            scp_is_free = False
                            break
        
            # If SCP is empty or only has vehicles with F=1, vehicle can proceed
            if scp_is_free and current_state.secondNode not in reserved_points:
                current_state.SA = 1
                current_state.F = 1  # Entering SCP
                return ControlSignal
        
        # Condition 3: SecondNode is in SCP and some point in SCP is reserved, but
        # other vehicle has not entered SCP (F=0) and there are spare points
        if in_scp:
            # Find spare points
            spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
            
            # Check if any point in SCP is reserved by another vehicle with F=0
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
            
            # If there are spare points and SecondNode is not reserved
            if spare_points and other_car_reserved_scp and current_state.secondNode not in reserved_points:
                current_state.SP = spare_points
                current_state.SA = 1
                current_state.F = 1
                
                # If vehicle has entered SCP (F=1) and firstNode is a spare point, remove it from SP
                if current_state.firstNode in spare_points:
                    current_state.SP.remove(current_state.firstNode)
                
                return ControlSignal
        
        # Handle deadlock
        # Check for Heading-on deadlock
        for pos in other_positions:
            # Heading-on deadlock: SecondNode of this vehicle is FirstNode of another vehicle and vice versa
            if current_state.secondNode == pos.FirstNode and pos.SecondNode == current_state.firstNode:
                # If current vehicle has F=1 (already entered SCP), use spare point
                if current_state.F == 1:
                    spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
                    if spare_points:
                        nearest_spare = spare_points[0]
                        # Move to spare point
                        ControlSignal.Road = DTO.road.Road(
                            current_state.firstNode,
                            nearest_spare,
                            BLL.road.Road.GetDistance(current_state.firstNode, nearest_spare),
                            0
                        )
                        # Add waitTime attribute
                        ControlSignal.waitTime = 0
                        return ControlSignal
                else:
                    # Other vehicle will move - current vehicle waits
                    current_state.SA = 2  # Waiting
                    # Keep current path but add wait time
                    ControlSignal.waitTime = 5  # Default wait time 5s
                    return ControlSignal
        
        # Check for Loop deadlock
        is_loop_deadlock = Constrains._check_loop_deadlock(TimeStart, current_state, other_positions)
        if is_loop_deadlock:
            spare_points = BLL.road.Road.allocate_spare_points(route_index, list_of_routes)
            if spare_points and current_state.F == 1:
                # Move to spare point
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
                # Wait in place
                current_state.SA = 2
                # Keep current path but add wait time
                ControlSignal.waitTime = 5  # Default wait time
                return ControlSignal
        
        # If no condition is satisfied - wait in place
        current_state.SA = 2
        # Keep current path but add wait time
        ControlSignal.waitTime = 5  # Default wait time
        return ControlSignal

    @staticmethod
    def _check_loop_deadlock(TimeStart, current_state, other_positions):
        """
        Check if a loop deadlock exists
        """
        visited = set()
        current = current_state.firstNode
        
        # Create dictionary mapping from firstNode to secondNode
        next_moves = {}
        for pos in other_positions:
            if pos.FirstNode and pos.SecondNode:
                next_moves[pos.FirstNode] = pos.SecondNode
        
        # Add current_state
        next_moves[current_state.firstNode] = current_state.secondNode
        
        # Check for cycle
        while current not in visited:
            visited.add(current)
            
            if current not in next_moves:
                return False
                
            current = next_moves[current]
            
            if current == current_state.firstNode:
                return True
        
        return False