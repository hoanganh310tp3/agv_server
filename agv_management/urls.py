from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
 
router.register('agv_data', views.AgvDataViewSet, basename="agv_data" )

urlpatterns = [
    path("", view=views.index),
]
urlpatterns += router.urls