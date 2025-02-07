from rest_framework import serializers

from .models import FarmerProfile,CropData


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FarmerProfile
        fields='__all__'

class CropDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=CropData
        fields='__all__'