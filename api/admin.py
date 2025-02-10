from django.contrib import admin
from .models import FarmerProfile,CropData,User

admin.site.register(FarmerProfile)
admin.site.register(CropData)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','role')
    # serach_fields=('username','email')
    list_filter=('role',)

# admin.site.register(User,UserAdmin)
