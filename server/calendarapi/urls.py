from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = [
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
    path('initiate_oauth/', initiate_oauth, name='initiate_oauth'),  
] + router.urls
