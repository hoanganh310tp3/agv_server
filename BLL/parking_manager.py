from typing import Dict, Optional
import threading

class ParkingManager:
    def __init__(self):
        # Fixed mapping of AGV IDs to their parking spots
        self._fixed_parking_spots = {
            "1": 0,  # AGV 1 parks at spot 0
            "2": 1,  # AGV 2 parks at spot 1
            "3": 2   # AGV 3 parks at spot 2
        }

    def get_agv_parking_spot(self, agv_id: str) -> Optional[int]:
        """
        Get the fixed parking spot for an AGV
        Args:
            agv_id: ID of the AGV
        Returns: parking spot number or None if AGV has no assigned spot
        """
        return self._fixed_parking_spots.get(agv_id)

# Global instance of parking manager
parking_manager = ParkingManager() 