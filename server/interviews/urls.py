from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, InterviewViewSet

app_name = 'interviews'

router = DefaultRouter()
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'interviews', InterviewViewSet)


# urlpatterns = [
#     # path('interviews/', include(router.urls)),
#     # path('availability/user_availabilities/<user_id>', AvailabilityViewSet.as_view({'get': 'list_user_availabilities'}), name='user-availability-list'),
#     # path('availability/delete_availabilites/<availability_id>', AvailabilityViewSet.as_view({'get': 'delete_availabilites'}), name='delete_availabilites'),

# ]

urlpatterns = router.urls