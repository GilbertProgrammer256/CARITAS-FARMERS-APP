from django.db import models


class FarmerProfile(models.Model):
    MALE='M'
    FEMALE='F'
    OTHERS='O'
    GENDER_CHOICES=(
        (MALE,'Male'),
        (FEMALE,'Female'),
        (OTHERS,'Others'),
    )

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    date_of_birth=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,default=OTHERS)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(null=True,blank=True)
    farm_location=models.CharField(max_length=255,null=True,blank=True)
    farm_size=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class CropData(models.Model):
    farmer=models.ForeignKey(FarmerProfile,on_delete=models.CASCADE,related_name='crops')
    crop_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    expected_yield = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_type} ({self.farmer.first_name} {self.farmer.last_name})"