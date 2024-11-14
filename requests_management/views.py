from django.shortcuts import render
from rest_framework import viewsets, generics
from django.http import HttpResponse
from .schedule import schedule_agv
from .serializers import OrderSerializer, ScheduleSerializer, CreateListModelMixin
from .models import order_data, schedule_data
from rest_framework.permissions import AllowAny
# from ManageRequests.schedule import schedule_agvs

# Create your views here.

class OrderView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    queryset = order_data.objects.all()

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