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

class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)
    