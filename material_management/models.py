from django.db import models

# Create your models here.

class material(models.Model):
    UNIT = (
        ('KG', 'Kilograms'),
        ('PCS', 'Piece')
    )

    material_id = models.BigAutoField(primary_key=True)
    material_name = models.CharField(max_length=32, default= 'none', unique= True)
    material_unit = models.CharField(max_length=16, default= 'KG', choices= UNIT)
    material_weight = models.IntegerField(default= 0)
    # material__unit_weight = models.IntegerField(default= 0)

    def __str__(self):
        return self.material_name
        # return "{Name} ({Weight}{Unit}/Unit)".format(Name = self.material_name, Weight = self.material_weight, Unit = self.material_unit)

    