from . import views
from django.urls import path

urlpatterns = [
    path('schedules/',views.request_schedule),
    path('sendOrders/',views.SendTaskView.as_view()),
]
