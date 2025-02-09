from rest_framework import serializers
from .models import FarmerProfile,CropData,User


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FarmerProfile
        fields=['id','first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email', 'farm_location', 'farm_size']

class CropDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=CropData
        fields = ['id', 'farmer', 'crop_type', 'planting_date', 'expected_yield', 'notes']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'data_collector'),
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name','')
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user



