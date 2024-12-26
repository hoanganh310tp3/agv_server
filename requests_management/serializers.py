from rest_framework import serializers
from .models import order_data, schedule_data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_data
        fields = '__all__'
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = schedule_data
        fields = '__all__'


    