from django.shortcuts import render
from rest_framework import viewsets

from .serializers import MaterialSerializer
from .models import material

# Create your views here.

from rest_framework.permissions import IsAuthenticated

class MaterialView(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = material.objects.all()
    permission_classes = [IsAuthenticated]
