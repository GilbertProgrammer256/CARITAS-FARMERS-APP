from rest_framework import serializers
from .models import FarmerProfile,CropData,User


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FarmerProfile
        fields='__all__'

class CropDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=CropData
        fields='__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'data_collector'),
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user



