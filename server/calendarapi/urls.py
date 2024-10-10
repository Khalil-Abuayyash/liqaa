# urls.py
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'availability', AvailabilityViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = [
    path('oauth2callback/', oauth2callback, name='oauth2callback'),  
    path('initiate_oauth/', initiate_oauth, name='initiate_oauth'),
    path('list_events/', list_events_view, name='list-events'),
    path('create_event/', create_event_view, name='create-event'),
]

urlpatterns += router.urls
