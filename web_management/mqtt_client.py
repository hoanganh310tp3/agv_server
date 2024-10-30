from agv_management.models import AGVData
from web_management.Database.DB_insert import insertAGVData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def on_message(client, userdata, message):
    if message.topic.startswith("AGV_Data/"):
        payload = message.payload
        agv_data = AGVData(payload)
        agv_data.decodeBuffer()
        inserted_data = insertAGVData(agv_data)
        
        # Send the new data to the WebSocket group
        async_to_sync(channel_layer.group_send)(
            "agv_data",
            {
                "type": "send_agv_data",
                "data": {
                    'data_id': inserted_data.data_id,
                    'car_id': inserted_data.car_id,
                    'agv_state': inserted_data.agv_state,
                    'agv_speed': inserted_data.agv_speed,
                    'agv_battery': inserted_data.agv_battery,
                    'previous_waypoint': inserted_data.previous_waypoint,
                    'distance': inserted_data.distance,
                    'next_waypoint': inserted_data.next_waypoint,
                    'distance_sum': inserted_data.distance_sum
                }
            }
        )