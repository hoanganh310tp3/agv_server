from django.urls import path
from agv_management.consumers import AGVDataConsumer

websocket_urlpatterns = [
    path('ws/agv_data/', AGVDataConsumer.as_asgi()),
]
