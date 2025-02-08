from django.urls import path,include
from .views import farmers_list,crop_list,farmers_detail,crop_detail,register_data_collector
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



urlpatterns = [
#auth and app management
path('api-auth/', include('rest_framework.urls')),
path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

path('register_data_collector/',register_data_collector,name='register_data_collector'),


path('farmers/',farmers_list),
path('farmers/<int:pk>/',farmers_detail),
path('crops/',crop_list),
path('crops/<int:pk>/',crop_detail),
path('register_data_collector/',register_data_collector),
]
