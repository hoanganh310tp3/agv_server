from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from web_management.Decode import buffer
from django.utils.translation import gettext_lazy as _
import struct

#identify handling
class agv_identify(models.Model):
    
    GUIDANCE_TYPE =(
        ('line_following','line_following'),
        ('image_processing','image_processing')
    )
    
    
    agv_id = models.IntegerField(primary_key=True, blank= False)
    max_speed = models.IntegerField(default= 0)
    battery_capacity = models.IntegerField(default= 0)
    max_load = models.IntegerField(default=0)
    guidance_type = models.CharField(max_length=255, blank=True, choices= GUIDANCE_TYPE) 
    parking_lot = models.IntegerField(default= 0, blank= False)
    is_active = models.BooleanField(default= True)  
    is_connected = models.BooleanField(default= True)

    def __str__(self):
        return "Vehicle ID: {ID}".format(ID= self.agv_id) + "." + "is_active: {state}".format(state = self.is_active) + "is_connected: {state}".format(state = self.is_connected)

class AGVHi():
    messageFrameAGVHi = [2, 2, 2, 4, 2, 4, 2, 2, 2, 2, 2, 2]
    
    payloadAGVHi = []
    bufferAGVHi = []
    def __init__(self, payload):
        self.payloadAGVHi = payload
        
    
    def decodeBuffer(self):
        self.bufferAGVHi = buffer.spliceBuffer(self.messageFrameAGVHi, self.payloadAGVHi)
        self.agv_id = int(self.bufferAGVHi[3], 16)
        self.maxSpeed = int(self.bufferAGVHi[4], 16)
        self.batteryCapacity = int(self.bufferAGVHi[5], 16)
        self.maxLoad = int(self.bufferAGVHi[6], 16)
        self.parkingLot = int(self.bufferAGVHi[7], 16)
        self.guidanceType = int(self.bufferAGVHi[8], 16)
        self.isActive = int(self.bufferAGVHi[9], 16)
        self.isConnected = int(self.bufferAGVHi[10], 16)
            
        

class agv_status(models.Model):
    state_id = models.IntegerField(default= 0)
    state_name = models.CharField(max_length= 16, default= 'None')
    
    def __str__(self):
        return "State #: {ID}".format(ID = self.state_id) + ":" + "state".format(state = self.state_name)


#data handling
class AGVData():
    class Position():
        def __init__(self, pNode=0, nNode=0, distance=0):
            self.prevNode = pNode
            self.nextNode = nNode
            self.distance = distance

    def __init__(self, payload):
        self.payloadAGVData = payload
        self.carPosition = self.Position()
        
    def decodeBuffer(self):
        try:
            # Convert bytes to list of integers for easier processing
            data = list(self.payloadAGVData)
            
            # Verify frame start byte (0x7A = 122 = 'z')
            if data[0] != 0x7A:
                raise ValueError(f"Invalid frame start byte: {hex(data[0])}")
            
            # Get frame length and message type
            frame_length = data[1]  # 0x0E = 14 bytes
            message_type = data[2]  # 0x02
            
            if message_type != 0x02:
                raise ValueError(f"Invalid message type: {hex(message_type)}")
            
            # Extract data fields
            self.carID = data[3]
            self.carState = data[4]
            self.carSpeed = data[5]
            self.carBatteryCap = data[6]
            self.carPosition.prevNode = data[7]
            self.carPosition.nextNode = data[8]
            self.carPosition.distance = (data[9] << 8) + data[10]  # Combine 2 bytes for distance
            self.distanceSum = (data[11] << 8) + data[12]  # Combine 2 bytes for distance_sum
            
            # Verify frame end byte (0x7F = 127)
            if data[-1] != 0x7F:
                raise ValueError(f"Invalid frame end byte: {hex(data[-1])}")
                
        except Exception as e:
            raise ValueError(f"Failed to decode payload: {str(e)}")
            
    def printOut(self):
        print(f"Car ID: {self.carID}")
        print(f"State: {self.carState}")
        print(f"Speed: {self.carSpeed}")
        print(f"Battery: {self.carBatteryCap}%")
        print(f"Position: {self.carPosition.prevNode} -> {self.carPosition.nextNode} ({self.carPosition.distance} units)")
        print(f"Total Distance: {self.distanceSum}")

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
    distance_sum = models.FloatField() 
    
    def __str__(self):
        return "Data ID: {ID}".format(ID = self.data_id)


#error handling
class agv_error(models.Model):
    error_id = models.IntegerField(default= 0, unique= True)
    timestamp = models.DateTimeField(default= timezone.now)
    car_id = models.IntegerField()
    error_msg = models.CharField(max_length=16, default='')
    previous_waypoint = models.IntegerField()
    next_waypoint = models.IntegerField()  
    order_number = models.IntegerField() #recently added

class AGVError():
    messageFrameAGVError = [2, 2, 2, 4, 2, 2, 4, 4, 2]
    payloadAGVError = []
    bufferAGVError = []

    def __init__(self, payload):
        self.payloadAGVError = payload
    
    def decodeBuffer(self):
        self.bufferAGVError = buffer.spliceBuffer(self.messageFrameAGVError, self.payloadAGVError)
        self.carID = int(self.bufferAGVError[3], 16)
        self.errorCode = int(self.bufferAGVError[4], 16)
        self.orderNum = int(self.bufferAGVError[5], 16)
        self.prevNode = int(self.bufferAGVError[6], 16)
        self.nextNode = int(self.bufferAGVError[7], 16)
    
        
