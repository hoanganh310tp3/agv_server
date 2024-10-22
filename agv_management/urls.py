from django.urls import path, include
from agv_management import views


urlpatterns = [
    path("", views.index),
]