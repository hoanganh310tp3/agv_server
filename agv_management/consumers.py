import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import agv_data
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
import asyncio
from contextlib import asynccontextmanager

# Tạo một Redis connection pool
from redis.asyncio import ConnectionPool
pool = ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)

@asynccontextmanager
async def get_redis_connection():
    from redis.asyncio import Redis
    redis = Redis(connection_pool=pool)
    try:
        yield redis
    finally:
        await redis.close()

class AGVDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("agv_data", self.channel_name)
        await self.accept()
        
        self.monitor_task = asyncio.create_task(self.monitor_data_changes())

    async def disconnect(self, close_code):
        if hasattr(self, 'monitor_task'):
            self.monitor_task.cancel()
        await self.channel_layer.group_discard("agv_data", self.channel_name)

    @database_sync_to_async
    def get_agv_data(self):
        return list(agv_data.objects.all().values('data_id', 'car_id', 'agv_state', 'agv_speed', 'agv_battery', 'previous_waypoint', 'distance', 'next_waypoint', 'distance_sum'))

    async def monitor_data_changes(self):
        last_data = None
        while True:
            try:
                current_data = await self.get_agv_data()
                
                if current_data != last_data:
                    await self.channel_layer.group_send(
                        "agv_data",
                        {
                            "type": "send_agv_data",
                            "data": current_data
                        }
                    )
                    last_data = current_data
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logging.error(f"Error in monitor_data_changes: {e}")
                await asyncio.sleep(1)

    async def send_agv_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data, default=str))

    async def receive(self, text_data):
        if text_data == "get_data":
            data = await self.get_agv_data()
            await self.send(text_data=json.dumps(data, default=str))

# Đảm bảo đóng connection pool khi ứng dụng kết thúc
import atexit

@atexit.register
def close_pool():
    asyncio.get_event_loop().run_until_complete(pool.disconnect())
