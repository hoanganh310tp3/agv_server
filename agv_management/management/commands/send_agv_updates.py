from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

class Command(BaseCommand):
    help = 'Sends AGV data updates to WebSocket clients'

    def handle(self, *args, **options):
        channel_layer = get_channel_layer()
        while True:
            async_to_sync(channel_layer.group_send)(
                'agv_data_group',
                {
                    'type': 'send_agv_data',
                }
            )
            time.sleep(1)  # Send updates every second
