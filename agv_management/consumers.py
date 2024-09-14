from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import agv_data, agv_identify, 
from .serializers import AgvDataserializer


class AgvdataConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset = agv_data.objects.all()
    serializer_class = AgvDataserializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(agv_data)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=AgvDataserializer(instance=instance).data, action=action.value)

    async def receive_json(self, content, **kwargs):
        action = content.get('action')
        if action == 'create':
            agv_data_instance = content.get('data', {})
            agv_identify_id = agv_data_instance.get('car_id')

            try:
                car_id = await agv_identify.objects.aget(agv_id=agv_identify_id) #notice here if error
                new_agv_data = agv_data(
                    car_id=car_id,
                    agv_state=agv_data_instance.get('agv_state'),
                    time_stamp=agv_data_instance.get('time_stamp'),
                    battery_consumption=agv_data_instance.get('battery_consumption'),
                    agv_speed=agv_data_instance.get('agv_speed'),
                    distance=agv_data_instance.get('distance'),
                    agv_battery=agv_data_instance.get('agv_battery'),
                    agv_position=agv_data_instance.get('agv_position'),
                    previous_waypoint=agv_data_instance.get('previous_waypoint'),
                    next_waypoint=agv_data_instance.get('next_waypoint')
                )
                await new_agv_data.asave()
                await self.send_json({'status': 'success', 'data': 'Agv data created successfully'})
            except agv_identify.DoesNotExist:
                await self.send_json({'status': 'error', 'errors': {'agv_identify': ['Invalid agv_identify ID']}})
        else:
            await self.send_json({'status': 'error', 'errors': {'action': ['Invalid action']}})


