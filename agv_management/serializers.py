from rest_framework import serializers
from .models import agv_identify, agv_data


class AgvIdentifySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = agv_identify
        fields = "__all__"
 
class AgvDataserializer(serializers.ModelSerializer):
    
    agv_identify = AgvIdentifySerializer()
    
    class Meta:
        model = agv_data
        fields = "__all__"
    