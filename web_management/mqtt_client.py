from agv_management.models import AGVData
from web_management.Database.DB_insert import insertAGVData

def on_message(client, userdata, message):
    if message.topic.startswith("AGV_Data/"):
        payload = message.payload
        agv_data = AGVData(payload)
        agv_data.decodeBuffer()
        insertAGVData(agv_data)
