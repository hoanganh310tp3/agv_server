from django.db import models

# Create your models here.

# class DB_MapData(models.Model):
#     pass

class station_data(models.Model):
    STATION_TYPE = (
        ('HOME', 'Parking station'),
        ('BAT', 'Charging station'),
        ('PICK', 'Pick up'),
        ('DROP', 'Drop') 
        # TO ADD MORE CUZ I CANT THINK OF ANYTHING RN
    )
    LOAD_TRANSFER = (
        ('AUTO', 'Automatic'),
        ('MAN', 'Manual')
    )
    
    station_id = models.IntegerField(primary_key= True, blank= False)
    station_node = models.IntegerField(default= 0)
    station_type = models.CharField(max_length=64, blank=True, choices= STATION_TYPE)
    load_transfer = models.CharField(max_length=64, blank=True, choices= LOAD_TRANSFER)
    is_active = models.BooleanField(default= False)

    def __str__(self):
        return "Station ID: {ID}".format(ID = self.station_id)