#  used in past but sometimes causing errors
# from . import mqtt
# mqtt.client.loop_start()

# suggestion fix

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_management.settings')
from . import mqtt
mqtt.client.loop_start()