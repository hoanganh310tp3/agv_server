from django.shortcuts import render
from rest_framework import viewsets

from .serializers import MaterialSerializer
from .models import material

# Create your views here.

class MaterialView(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = material.objects.all()