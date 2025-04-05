from django.db import models
from django.utils import timezone
from material_management.models import material
from users_management.models import User
# Create your models here.  
    
class order_data(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    order_number = models.IntegerField(default=0) # sửa lại
    order_date = models.DateField()
    load_name = models.CharField(max_length=16, default='none')
    load_amount = models.PositiveIntegerField(default=0)
    load_weight = models.IntegerField(default=0)
    start_time = models.CharField(max_length=16, default='00:00:00')
    start_point = models.PositiveBigIntegerField(default=0)
    end_point = models.PositiveBigIntegerField(default=0)
    user_name = models.ForeignKey(User, to_field='name', on_delete=models.CASCADE, null=True)
    is_scheduled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Request #{self.order_number}"
 
class schedule_data(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    order_number = models.IntegerField(default=0)
    order_date = models.DateField()
    load_name = models.CharField(max_length=16, default='none')
    load_weight = models.FloatField(default= 0)
    load_amount = models.PositiveIntegerField(default=0)
    agv_id = models.IntegerField(default=0)
    est_energy = models.IntegerField()
    est_distance = models.FloatField()
    est_start_time = models.CharField(max_length=16, default='00:00:00')
    est_end_time = models.CharField(max_length=16, default='00:00:00')
    start_point = models.IntegerField(default=0)
    end_point = models.IntegerField(default=0)
    is_processed = models.BooleanField(default=False)
    instruction_set  = models.JSONField()
    session_id = models.CharField(max_length=14, default='00000000000000')

    def __str__(self):
        return "Order #{ID}".format(ID =self.order_number)

    