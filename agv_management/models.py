from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from web_management.Decode import buffer
from django.utils.translation import gettext_lazy as _

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
# class AGVData():
#     class Position():
#         def __init__(self, pNode, nNode, distance):
#             self.prevNode = pNode
#             self.nextNode = nNode
#             self.distance = distance

#     messageFrameAGVData = [1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1]
#     payloadAGVData = []
#     bufferAGVData = []
#     carPosition = Position
    
#     def __init__(self, payload):
#         self.payloadAGVData = payload
    
#     def decodeBuffer(self):
#         self.bufferAGVData = buffer.spliceBuffer(self.messageFrameAGVData, self.payloadAGVData)
#         # Decode trực tiếp từ bytes
#         self.carID = int.from_bytes(self.bufferAGVData[3], byteorder='big')
#         self.carState = int.from_bytes(self.bufferAGVData[4], byteorder='big')
#         self.carBatteryCap = int.from_bytes(self.bufferAGVData[5], byteorder='big')
#         self.carSpeed = int.from_bytes(self.bufferAGVData[6], byteorder='big')
#         self.carPosition.prevNode = int.from_bytes(self.bufferAGVData[7], byteorder='big')
#         self.carPosition.nextNode = int.from_bytes(self.bufferAGVData[8], byteorder='big')
#         self.carPosition.distance = int.from_bytes(self.bufferAGVData[9], byteorder='big')   
#         self.distanceSum = int.from_bytes(self.bufferAGVData[10], byteorder='big')
#         self.checkSum = int.from_bytes(self.bufferAGVData[11], byteorder='big')
        
    
#     def printOut(self):
#         print("carId:", self.carID, "state:", self.carState, "battery capacity:", self.carBatteryCap/100, "speed:", self.carSpeed/100, "current position:",
#                     self.carPosition.prevNode, self.carPosition.nextNode, self.carPosition.distance/100, "total energy:", self.distanceSum/100)

#     # def check_sum(self):
#     #     checkSumValue = self.carID + self.carState + self.carBatteryCap + self.carSpeed + self.carPosition.prevNode + self.carPosition.nextNode + self.carPosition.distance + self.distanceSum + self.checkSum
#     #     if (checkSumValue + self.check_sum == 65536):
#     #         return True # packet valid
#     #     else:
#     #         return False # packet invalid
             
class AGVData():
    class Position():
        def __init__(self, pNode, nNode, distance):
            self.prevNode = pNode
            self.nextNode = nNode
            self.distance = distance

    # Frame chỉ chứa thông tin cơ bản và prevNode
    messageFrameAGVData = [1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1]
    payloadAGVData = []
    bufferAGVData = []
    carPosition = Position
    
    def __init__(self, payload):
        self.payloadAGVData = payload
    
    def decodeBuffer(self):
        self.bufferAGVData = buffer.spliceBuffer(self.messageFrameAGVData, self.payloadAGVData)
        
        # Chỉ lấy thông tin prevNode từ frame
        self.carPosition.prevNode = int.from_bytes(self.bufferAGVData[3], byteorder='big')
        
        # Set các giá trị mặc định cho các thông tin khác
        self.carID = 0  # Giả sử carID mặc định là 0
        self.carState = 0  # Giả sử trạng thái mặc định là 0
        self.carBatteryCap = 0  # Giả sử battery mặc định là 0
        self.carSpeed = 0  # Giả sử tốc độ mặc định là 0
        self.carPosition.nextNode = 0  # Giả sử nextNode mặc định là 0
        self.carPosition.distance = 0  # Giả sử distance mặc định là 0
        self.distanceSum = 0  # Giả sử distanceSum mặc định là 0
        self.checkSum = 0  # Giả sử checkSum mặc định là 0


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


#error handling
class agv_error(models.Model):
    error_id = models.IntegerField(default= 0, unique= True)
    timestamp = models.DateTimeField(default= timezone.now)
    car_id = models.IntegerField()
    error_msg = models.CharField(max_length=16, default='')
    previous_waypoint = models.IntegerField()
    next_waypoint = models.IntegerField()  
    order_number = models.IntegerField() #recently added


    # Thay đổi messageFrameAGVError để phản ánh số byte thực tế
    # 2 -> 1 byte, 4 -> 2 bytes
    # messageFrameAGVError = [1, 1, 1, 2, 1, 1, 2, 2, 1]
    # payloadAGVError = []
    # bufferAGVError = []

    # def __init__(self, payload):
    #     self.payloadAGVError = payload
    
    # def decodeBuffer(self):
    #     self.bufferAGVError = buffer.spliceBuffer(self.messageFrameAGVError, self.payloadAGVError)
    #     # Decode trực tiếp từ bytes
    #     self.carID = int.from_bytes(self.bufferAGVError[3], byteorder='big')
    #     self.errorCode = int.from_bytes(self.bufferAGVError[4], byteorder='big')
    #     self.orderNum = int.from_bytes(self.bufferAGVError[5], byteorder='big')
    #     self.prevNode = int.from_bytes(self.bufferAGVError[6], byteorder='big')
    #     self.nextNode = int.from_bytes(self.bufferAGVError[7], byteorder='big')
    
        
class AGVError():
    # Frame chỉ chứa thông tin cơ bản, errorCode và prevNode
    messageFrameAGVError = [1, 1, 1, 2, 1, 1, 2, 2, 1]
    payloadAGVError = []
    bufferAGVError = []

    def __init__(self, payload):
        self.payloadAGVError = payload
    
    def decodeBuffer(self):
        self.bufferAGVError = buffer.spliceBuffer(self.messageFrameAGVError, self.payloadAGVError)
        
        # Chỉ lấy errorCode và prevNode từ frame
        self.errorCode = int.from_bytes(self.bufferAGVError[3], byteorder='big')
        self.prevNode = int.from_bytes(self.bufferAGVError[4], byteorder='big')
        
        # Set các giá trị mặc định cho các thông tin khác
        self.carID = 0  # Giả sử carID mặc định là 0
        self.orderNum = 0  # Giả sử orderNum mặc định là 0
        self.nextNode = 0  # Giả sử nextNode mặc định là 0