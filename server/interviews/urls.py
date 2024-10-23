from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, InterviewViewSet

app_name = 'interviews'

router = DefaultRouter()
router.register(r'availability', AvailabilityViewSet)
router.register(r'interviews', InterviewViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += router.urls