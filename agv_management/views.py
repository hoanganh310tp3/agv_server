from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import agv_data, agv_identify
from .serializers import AgvIdentifySerializer, AgvDataserializer


# For Agv_identify restful API
class AgvIdentifyViewSet(ModelViewSet):
    serializer_class = AgvIdentifySerializer
    queryset = agv_identify.objects.all()
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print("Sending AGV data:", serializer.data)
        return Response(serializer.data)

# For Agv_data websocket 
class AgvDataViewSet(ModelViewSet):
    serializer_class = AgvDataserializer
    queryset = agv_data.objects.all()
    permission_classes = [AllowAny]

def index(request):
    return render(request, "agv_management/index.html")

def agv_data_realtime(request):
    return render(request, 'agv_data_realtime.html')
