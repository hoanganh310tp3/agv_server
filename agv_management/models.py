from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class agv_identify(models.Model):
    
    GUIDANCE_TYPE =(
        ('line_following','line_following'),
        ('image_processing','image_processing')
    )
    
    agv_id = models.IntegerField(primary_key=True, blank=False)  
    maximum_speed = models.IntegerField(default= 0)
    parking_lot = models.IntegerField(default= 0, blank=False)
    battery_capacity = models.IntegerField(default= 0)
    maximum_load = models.IntegerField(default=0)
    guidance_type = models.CharField(max_length=255, blank=True, choices= GUIDANCE_TYPE)  
    operation = models.BooleanField(default= True)  
    connection = models.BooleanField(default= True)

    def __str__(self):
        return "Vehicle ID: {ID}".format(ID= self.agv_id) + "." + "Operation: {state}".format(state = self.operation) + "Connection: {state}".format(state = self.connection)

class agv_status(models.Model):
    state_id = models.IntegerField(default= 0)
    state_name = models.CharField(max_length= 16, default= 'None')
    
    def __str__(self):
        return "State #: {ID}".format(ID = self.state_id) + ":" + "state".format(state = self.state_name)
    
class agv_data(models.Model):
    data_id = models.BigAutoField(primary_key=True) 
    car_id = models.ForeignKey(agv_identify, on_delete=models.CASCADE) #many-to-one relationship test
    #car_id = models.IntegerField()
    car_state = models.IntegerField()
    agv_speed = models.FloatField()
    distance = models.FloatField()
    agv_battery = models.FloatField()
    agv_position = models.FloatField()
    previous_waypoint = models.IntegerField()
    next_waypoint = models.IntegerField()
    time_stamp = models.DateTimeField(blank= True)
    battery_consumption = models.IntegerField()
    

    def __str__(self):
        return "Data ID: {ID}".format(ID = self.data_id)
    
class agv_error(models.Model):
    error_id = models.IntegerField(default= 0, unique= True)
    timestamp = models.DateTimeField(default= timezone.now)
    car_id = models.ForeignKey(agv_identify, on_delete=models.CASCADE) #many-to-one relationship test 
    #car_id = models.IntegerField() 
    error_msg = models.CharField(max_length=16, default='')
    previous_waypoint = models.IntegerField()
    next_waypoint = models.IntegerField()  



