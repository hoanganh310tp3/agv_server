from . import views
from django.urls import path

urlpatterns = [
    path('schedule/',views.request_schedule),
]

