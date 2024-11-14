from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import MaterialSerializer
from .models import material

# Create your views here.
class MaterialView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = MaterialSerializer
    queryset = material.objects.all()
    
