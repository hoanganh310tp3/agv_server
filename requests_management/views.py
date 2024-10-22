from django.shortcuts import render
from rest_framework import viewsets, generics, status
from django.http import HttpResponse
from .schedule import schedule_agv
from .serializers import OrderSerializer, ScheduleSerializer, CreateListModelMixin
from .models import order_data, schedule_data
# from ManageRequests.schedule import schedule_agvs

# Create your views here.

class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = order_data.objects.all()

class ScheduleView(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = schedule_data.objects.all()

class SendTaskView(CreateListModelMixin, generics.CreateAPIView):
    serializer_class = OrderSerializer

def request_schedule(request):
    response = HttpResponse()
    if request.method == 'GET':
        schedule_agv()
        response = HttpResponse("Schedule created successfully!")
    else:
        pass
    return response