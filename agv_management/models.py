from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from web_management.Decode import buffer
from django.utils.translation import gettext_lazy as _

class agv_identify(models.Model):
    
    GUIDANCE_TYPE =(
        ('line_following','line_following'),
        ('image_processing','image_processing')
    )
    
    
    agv_id = models.IntegerField(primary_key=True, blank=False)  
    max_speed = models.IntegerField(default= 0)
    battery_capacity = models.IntegerField(default= 0)
    max_load = models.IntegerField(default=0)
    guidance_type = models.CharField(max_length=255, blank=True, choices= GUIDANCE_TYPE)  
    is_busy = models.BooleanField(default= True)  
    is_connected = models.BooleanField(default= True)

    def __str__(self):
        return "Vehicle ID: {ID}".format(ID= self.agv_id) + "." + "Operation: {state}".format(state = self.operation) + "Connection: {state}".format(state = self.connection)

class agv_status(models.Model):
    state_id = models.IntegerField(default= 0)
    state_name = models.CharField(max_length= 16, default= 'None')
    
    def __str__(self):
        return "State #: {ID}".format(ID = self.state_id) + ":" + "state".format(state = self.state_name)

#old code
# class AGVData():
#     class Position():
#         def __init__(self, pNode, nNode, distance):
#             self.prevNode = pNode
#             self.nextNode = nNode
#             self.distance = distance

#     messageFrameAGVData = messageFrameAGVData = [1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1]
#     payloadAGVData = []
#     bufferAGVData = []
#     carPosition = Position

#     def __init__(self, payload):
#         self.payloadAGVData = payload
    
#     def decodeBuffer(self):
#         self.carID = int.from_bytes(self.bufferAGVData[3], byteorder= 'little')
#         self.carState = int.from_bytes(self.bufferAGVData[4], byteorder= 'little')
#         self.carBatteryCap = int.from_bytes(self.bufferAGVData[5], byteorder= 'little')
#         self.carSpeed = int.from_bytes(self.bufferAGVData[6], byteorder= 'little')
#         self.carPosition.prevNode = int.from_bytes(self.bufferAGVData[7], byteorder= 'little')
#         self.carPosition.nextNode = int.from_bytes(self.bufferAGVData[8], byteorder= 'little')
#         self.carPosition.distance = int.from_bytes(self.bufferAGVData[9], byteorder= 'little')   
#         self.energySum = int.from_bytes(self.bufferAGVData[10], byteorder= 'little')
#         self.distanceSum = int.from_bytes(self.bufferAGVData[11], byteorder= 'little')
#         self.checkSum = int.from_bytes(self.bufferAGVData[12], byteorder= 'little')
    
    

#     def check_sum(self):
#         checkSumValue = self.carID + self.carState + self.carBatteryCap + self.carSpeed + self.carPosition.prevNode + self.carPosition.nextNode + self.carPosition.distance + self.distanceSum + self.checkSum
#         if (checkSumValue + self.check_sum == 65536):
#             return True # packet valid
#         else:
#             return False # packet invalid

class AGVData():
    class Position():
        def __init__(self, pNode, nNode, distance):
            self.prevNode = pNode
            self.nextNode = nNode
            self.distance = distance

    messageFrameAGVData = [2, 2, 2, 4, 2, 4, 2, 4, 4, 4, 4, 4, 2]
    payloadAGVData = []
    bufferAGVData = []
    carPosition = Position
    
    def __init__(self, payload):
        self.payloadAGVData = payload
    
    def decodeBuffer(self):
        self.bufferAGVData = buffer.spliceBuffer(self.messageFrameAGVData, self.payloadAGVData)
        self.carID = int(self.bufferAGVData[3], 16)
        self.carState = int(self.bufferAGVData[4], 16)
        self.carBatteryCap = int(self.bufferAGVData[5], 16)
        self.carSpeed = int(self.bufferAGVData[6], 16)
        self.carPosition.prevNode = int(self.bufferAGVData[7], 16)
        self.carPosition.nextNode = int(self.bufferAGVData[8], 16)
        self.carPosition.distance = int(self.bufferAGVData[9], 16)   
        self.distanceSum = int(self.bufferAGVData[10], 16)
        self.checkSum = int(self.bufferAGVData[11], 16)
    
    def printOut(self):
        print("carId:", self.carID, "state:", self.carState, "battery capacity:", self.carBatteryCap/100, "speed:", self.carSpeed/100, "current position:",
                    self.carPosition.prevNode, self.carPosition.nextNode, self.carPosition.distance/100, "total energy:", self.distanceSum/100)

    def check_sum(self):
        checkSumValue = self.carID + self.carState + self.carBatteryCap + self.carSpeed + self.carPosition.prevNode + self.carPosition.nextNode + self.carPosition.distance + self.energySum + self.distanceSum + self.checkSum
        if (checkSumValue + self.check_sum == 65536):
            return True # packet valid
        else:
            return False # packet invalid
             

class agv_data(models.Model):
    data_id = models.BigAutoField(primary_key=True) 
    car_id = models.IntegerField()
    agv_state = models.IntegerField()
    agv_speed = models.FloatField()
    agv_battery = models.FloatField()
    current_position = AGVData.Position
    previous_waypoint = models.IntegerField()
    distance = models.FloatField(default=0.0)
    next_waypoint = models.IntegerField()
    time_stamp = models.DateTimeField(blank= True)
    distance_sum = models.FloatField() # recently added
    
    def __str__(self):
        return "Data ID: {ID}".format(ID = self.data_id)



class agv_error(models.Model):
    error_id = models.IntegerField(default= 0, unique= True)
    timestamp = models.DateTimeField(default= timezone.now)
    car_id = models.ForeignKey(agv_identify, on_delete=models.CASCADE) #many-to-one relationship 
    error_msg = models.CharField(max_length=16, default='')
    previous_waypoint = models.IntegerField()
    next_waypoint = models.IntegerField()  
    order_number = models.IntegerField() #recently added

#buffer


class AGVError():
    messageFrameAGVError = [1, 1, 1, 2, 1, 1, 2, 2, 1]
    payloadAGVError = []
    bufferAGVError = []

    def __init__(self, payload):
        self.payloadAGVError = payload
    
    def decodeBuffer(self):
        self.bufferAGVError = buffer.spliceBuffer(self.messageFrameAGVError, self.payloadAGVError)
        self.carID = int.from_bytes(self.bufferAGVError[3], byteorder= 'little')
        self.errorCode = int.from_bytes(self.bufferAGVError[4], byteorder= 'little')
        self.orderNum = int.from_bytes(self.bufferAGVError[5], byteorder= 'little')
        self.prevNode = int.from_bytes(self.bufferAGVError[6], byteorder= 'little')
        self.nextNode = int.from_bytes(self.bufferAGVError[7], byteorder= 'little')
