from django.urls import path,include
from .views import farmers_list,crop_list,farmers_detail,crop_detail




urlpatterns = [
path('farmers/',farmers_list),
path('farmers/<int:pk>/',farmers_detail),
path('crops/',crop_list),
path('crops/<int:pk>/',crop_detail)
]
