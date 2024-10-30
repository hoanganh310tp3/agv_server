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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("agv_data", self.channel_name)

    @database_sync_to_async
    def get_agv_data(self):
        return list(agv_data.objects.all().values('data_id', 'car_id', 'agv_state', 'agv_speed', 'agv_battery', 'previous_waypoint', 'distance', 'next_waypoint', 'distance_sum'))

    async def send_agv_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data, default=str))

    async def receive(self, text_data):
        if text_data == "get_data":
            data = await self.get_agv_data()
            formatted_data = json.dumps(data, default=str)
            print("Sending data:", formatted_data)  # Debug log
            await self.send(text_data=formatted_data)

# Đảm bảo đóng connection pool khi ứng dụng kết thúc
import atexit

@atexit.register
def close_pool():
    asyncio.get_event_loop().run_until_complete(pool.disconnect())
