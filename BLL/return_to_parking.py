from typing import Optional, List, Tuple
from .parking_manager import parking_manager
from .road import Road
import DTO.schedule
from .position import Position

class ReturnToParkingHandler:
    def __init__(self):
        self._schedule = None  # Will be set later to avoid circular import

    def set_schedule(self, schedule_class):
        """Set the schedule class to use"""
        self._schedule = schedule_class

    def find_best_parking_path(self, current_pos: int) -> Tuple[Optional[int], Optional[List[int]]]:
        """
        Find the best available parking spot and path to it
        Args:
            current_pos: Current position of AGV
        Returns:
            Tuple of (parking spot number, path to parking spot) or (None, None) if no spot available
        """
        # Try each parking spot (0,1,2)
        min_distance = float('inf')
        best_spot = None
        best_path = None

        for spot in [0, 1, 2]:
            if parking_manager.is_spot_available(spot):
                # Calculate distance to this parking spot
                distance = Road.GetDistance(current_pos, spot)
                if distance < min_distance:
                    min_distance = distance
                    best_spot = spot
                    best_path = [current_pos, spot]  # Direct path from current position to parking

        return best_spot, best_path

    async def handle_return_to_parking(self, agv_id: str, current_pos: int) -> bool:
        """
        Handle the process of returning an AGV to a parking spot
        Args:
            agv_id: ID of the AGV
            current_pos: Current position of AGV
        Returns:
            True if successfully assigned and path created, False otherwise
        """
        # Find best available parking spot and path
        parking_spot, path = self.find_best_parking_path(current_pos)
        
        if parking_spot is None or path is None:
            return False

        # Try to assign the parking spot
        if parking_manager.assign_parking_spot(agv_id):
            # Create a new schedule for returning to parking
            positions = [Position(pos) for pos in path]
            if self._schedule:
                schedule_obj = DTO.schedule.Schedule()
                schedule_obj.Car = DTO.agv_car.AGVCar()
                schedule_obj.Car.CarId = agv_id
                await self._schedule.add_schedule(agv_id, positions, is_parking=True)
            return True
            
        return False

    def release_agv_from_parking(self, agv_id: str) -> None:
        """
        Release an AGV from its parking spot when it starts a new order
        Args:
            agv_id: ID of the AGV
        """
        parking_manager.release_parking_spot(agv_id) 