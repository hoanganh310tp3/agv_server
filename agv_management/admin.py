from django.contrib import admin
from .models import agv_data, agv_identify, agv_status
# Register your models here.
admin.site.register(agv_status)
admin.site.register(agv_identify)
admin.site.register(agv_data)