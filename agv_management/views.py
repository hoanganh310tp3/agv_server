from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import viewsets

from .models import agv_data, agv_identify
from .serializers import AgvIdentifySerializer, AgvDataserializer

# For Agv_identify restfulapi
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def agv_management_list(request):
    if request.method == 'GET':
        data = agv_identify.objects.all()

        serializer = AgvIdentifySerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgvIdentifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny])
def agv_management_detail(request, pk):
    try:
        agv = agv_identify.objects.get(pk=pk)
    except agv_identify.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer =  AgvIdentifySerializer(agv, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        agv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# For Agv_data websocket 

class AgvDataViewSet(viewsets.ModelViewSet):
    
    serializer_class = AgvDataserializer
    queryset = agv_data.objects.all()
    permission_classes = [AllowAny]
    
def index(request):
    return render(request, "agv_management/index.html")