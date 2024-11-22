"""
URL configuration for web_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from agv_management.views import AgvIdentifyViewSet, agv_data_realtime
from requests_management.views import OrderView, ScheduleView
from material_management.views import MaterialView
from users_management.views import LoginView


router = routers.DefaultRouter()
router.register(r'agv_identify', AgvIdentifyViewSet, 'Manage AGVs')
router.register(r'orders', OrderView, 'Manage Orders')
router.register(r'schedules', ScheduleView, 'Manage Schedules')
router.register(r'material', MaterialView, 'Manage Materials')

urlpatterns = [
    #Non-API related rows
    path('admin/', admin.site.urls),
    path('requests_management/',include('requests_management.urls')),
    path('agv_management/', include('agv_management.urls')),
    
    #API related rows
    path("api/", include('users_management.urls')),
    path('api/', include(router.urls)),
    path('agv-data-realtime/', agv_data_realtime, name='agv_data_realtime'),
    path('api/login', LoginView.as_view(), name='login'),
]
