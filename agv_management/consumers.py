import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import agv_data

class AGVDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_latest_agv_data(self):
        return agv_data.objects.latest('time_stamp')

    async def send_agv_data(self):
        latest_data = await self.get_latest_agv_data()
        await self.send(text_data=json.dumps({
            'car_id': latest_data.car_id,
            'agv_state': latest_data.agv_state,
            'agv_speed': latest_data.agv_speed,
            'agv_battery': latest_data.agv_battery,
            'previous_waypoint': latest_data.previous_waypoint,
            'next_waypoint': latest_data.next_waypoint,
            'distance': latest_data.distance,
            'distance_sum': latest_data.distance_sum,
            'time_stamp': latest_data.time_stamp.isoformat(),
        }))
