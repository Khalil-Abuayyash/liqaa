from django.urls import path, include
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)

app_name = 'users'

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'), # access - login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh 
]