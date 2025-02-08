from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import FarmerProfile,CropData
from .serializers import CropDataSerializer,FarmerProfileSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def register_data_collector(request):
    if request.user.role !='admin':
        return Response({'error':'Only admin are allowed to create data collector account.'})
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save(role='data_collector')
        return Response({"message":"Data collector account created successfully","username":user.username,"role":user.role},status=status.HTTP_201_CREATED)
    return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def farmers_list(request):
    if request.user.role not in ['admin','data_collector']:
        return Response({'error':'You donot have permission to perform this action'},status=403)
    
    if request.method=='GET':
        farmers=FarmerProfile.objects.filter(created_by=request.user)
        serializers=FarmerProfileSerializer(farmers,many=True)
        return Response(serializers.data)
    elif request.method=='POST':
        serializers=FarmerProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(created_by=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def farmers_detail(request,pk):
    if request.user.role not in ['admin','data_collector']:
        return Response({'error':'You donot have permission to perform this action'},status=403)
    try:
        farmer=FarmerProfile.objects.get(pk=pk,created_by=request.user)
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
@permission_classes([IsAuthenticated])
def crop_list(request):
    if request.user.role not in ['admin','data_collector']:
        return Response({'error':'You donot have permission to perform this action'},status=403)
    
    if request.method=='GET':
        crops=CropData.objects.filter(created_by=request.user)
        serializers=CropDataSerializer(crops,many=True)
        return Response(serializers.data)
    elif request.method=='POST':
        serializers=CropDataSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(created_by=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def crop_detail(request,pk):
    if request.user.role not in ['admin','data_collector']:
        return Response({'error':'You donot have permission to perform this action'},status=403)
    try:
        crop=CropData.objects.get(pk=pk,created_by=request.user)
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
    
    
