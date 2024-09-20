from django.db import models
from django.utils import timezone

# Create your models here.

class schedule_data(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_number = models.IntegerField(default=0)
    order_date = models.DateField()
    load_name = models.CharField(max_length=16, default='none')
    load_weight = models.FloatField(default= 0)
    agv_id = models.IntegerField(default=0)
    battery_loss = models.IntegerField()
    total_trip = models.FloatField()
    start_time = models.CharField(max_length=16, default='00:00:00')
    end_time = models.CharField(max_length=16, default='00:00:00')
    begin_waypoint = models.IntegerField(default=0)
    end_waypoint = models.IntegerField(default=0)
    process_status = models.BooleanField(default=False)
    
    def __str__(self):
        return "Order #{ID}".format(ID =self.order_number)  
    
class order_data(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    order_date = models.DateField()
    order_number = models.IntegerField(default=0)
    load_name = models.CharField(max_length=16, default= 'none' )  
    load_amount = models.PositiveIntegerField(default= 0)
    load_weight = models.IntegerField(default= 0)
    start_time = models.CharField(max_length=16, default= '00:00:00')
    begin_waypoint = models.PositiveBigIntegerField(default= 0)
    end_waypoint = models.PositiveBigIntegerField(default= 0)
    schedule_status = models.BooleanField(default=False)
    process_status = models.BooleanField(default=False)

    def __str__(self):
     return "Request #{ID}".format(ID = self.order_number)

    