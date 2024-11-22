
from rest_framework import viewsets, generics, status
from django.http import HttpResponse
from .schedule import schedule_agv
from .serializers import OrderSerializer, ScheduleSerializer, CreateListModelMixin
from .models import order_data, schedule_data
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Create your views here.

class OrderView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    queryset = order_data.objects.all()
    
    def create(self, request):
        if isinstance(request.data, list):
            # Handle multiple objects
            serializer = OrderSerializer(data=request.data, many=True)
        else:
            # Handle single object
            serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ScheduleSerializer
    queryset = schedule_data.objects.all()

class SendTaskView(CreateListModelMixin, generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

def request_schedule(request):
    response = HttpResponse()
    if request.method == 'GET':
        schedule_agv()
        response = HttpResponse("Schedule created successfully!")
    else:
        pass
    return response