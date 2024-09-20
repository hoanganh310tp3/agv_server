from django.contrib import admin
from .models import schedule_data, order_data

# Register your models here.

admin.site.register(schedule_data)
admin.site.register(order_data)