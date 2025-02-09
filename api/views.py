from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import FarmerProfile,CropData,User
from .serializers import CropDataSerializer,FarmerProfileSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin,IsOwnerOrAdmin
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend  
from django_filters import rest_framework as filters
from rest_framework_simplejwt.tokens import RefreshToken

class CustomPagination(PageNumberPagination):
    page_size=5
    page_size_query_param='page_size'
    max_page_size=50

    def get_paginated_response(self, data):
        return Response({
            'count':self.page.paginator.count,
            'next':self.get_next_link(),
            'previous':self.get_previous_link(),
            'results':data
        })
   


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def register_data_collector(request):
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
        gender=request.query_params.get('gender')
        farm_location=request.query_params.get('farm_location')
        if gender:
            farmers=farmers.filter(gender=gender)
        if farm_location:
            farmers=farmers.filter(farm_location__icontains=farm_location)

        paginator=CustomPagination()
        paginated_farmers=paginator.paginate_queryset(farmers,request)
        serializers=FarmerProfileSerializer(paginated_farmers,many=True)
        return paginator.get_paginated_response(serializers.data)
    
    elif request.method=='POST':
        serializers=FarmerProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(created_by=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def farmers_detail(request,pk):
    farmer=get_object_or_404(FarmerProfile,pk=pk)
    
    if not IsOwnerOrAdmin().has_object_permission(request,None,farmer):
        return Response({'error':'You donot have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
    
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

        #filtering
        crop_type=request.query_params.get('crop_type)')
        planting_date=request.query_params.get('planting_date')
        if crop_type:
            crops=crops.filter(crop_type=crop_type)
        if planting_date:
            crops=crops.filter(planting_date=planting_date)
        paginator=CustomPagination()
        paginated_crops=paginator.paginate_queryset(crops,request)
        serializers=CropDataSerializer(paginated_crops,many=True)
        return paginator.get_paginated_response(serializers.data)
    elif request.method=='POST':
        serializers=CropDataSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(created_by=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def crop_detail(request,pk):
    crop=get_object_or_404(CropData,pk=pk)
    if not IsOwnerOrAdmin().has_object_permission(request,None,crop):
        return Response({'error':'You donot have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
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
    
    
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summery(request):
    if request.user.role !='admin':
        return Response({'error':'You donot have permission to perform this action'},status=403)
    total_farmers=FarmerProfile.objects.count()
    total_crops=CropData.objects.count()
    data_collectos_count=User.objects.filter(role='data_collector').count()

    #farmers registered per month
    farmers_by_month=(
        FarmerProfile.objects.values('created_at__month')
        .annotate(count=Count('id'))
        .order_by('created_at__month')
    )

    #crops by type (for a pie chart)
    crops_by_type=(
        CropData.objects.values('crop_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    response_data={
        'total_farmers':total_farmers,
        'total_crops':total_crops,
        'data_collectors_count':data_collectos_count,
        'farmers_by_month':farmers_by_month,
        'crops_by_type':crops_by_type,
    }
    return Response(response_data)



#logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token=request.date=['refresh']
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message':'Sucessfully logged out'},status=200)
    except Exception as e:
        return Response({'error':'Failed to logout'},status=400)