from rest_framework import serializers
from .models import material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = material
        fields = ('material_id', 'material_name', 'material_unit', 'material_weight',)