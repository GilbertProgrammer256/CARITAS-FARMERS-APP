from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FarmerProfile,CropData
from .serializers import CropDataSerializer,FarmerProfileSerializer


@api_view(['GET','POST'])
def farmers_list(request):
    if request.method=='GET':
        farmers=FarmerProfile.objects.all()
        serializers=FarmerProfileSerializer(farmers,many=True)
        return Response(serializers.data)
    elif request.method=='POST':
        serializers=FarmerProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
def farmers_detail(request,pk):
    try:
        farmer=FarmerProfile.objects.get(pk=pk)
    except FarmerProfile.DoesNotExist:
        return Response({'error':'Farmer not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=FarmerProfileSerializer(farmer)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=FarmerProfileSerializer(farmer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        farmer.delete()
        return Response({'message':'Farmer deleted successfully'},status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def crop_list(request):
    if request.method=='GET':
        crops=CropData.objects.all()
        serializers=CropDataSerializer(crops,many=True)
        return Response(serializers.data)
    elif request.method=='POST':
        serializers=CropDataSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def crop_detail(request,pk):
    try:
        crop=CropData.objects.get(pk=pk)
    except CropData.DoesNotExist:
        return Response({'error':'Crop not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=CropDataSerializer(crop)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=CropDataSerializer(crop,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        crop.delete()
        return Response({'message':'Crop deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
    
