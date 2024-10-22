from rest_framework import serializers
from .models import agv_identify, agv_data


class AgvIdentifySerializer(serializers.ModelSerializer):    
    class Meta:
        model = agv_identify
        fields = ('agv_id', 'battery_capacity', 'maximum_load', 'guidance_type', 'load_transfer', 'operation' , 'connection')
 
class AgvDataserializer(serializers.ModelSerializer):
    
    class Meta:
        model = agv_data
        fields = "__all__"
    