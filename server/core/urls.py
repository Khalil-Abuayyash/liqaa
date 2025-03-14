
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # interviews app
    path('api/', include('interviews.urls', namespace='interviews')),
    # This path for calendar api / Hamada 
    path('api/calendarapi/', include('calendarapi.urls')),

    # Tokens
    path('api/token/', include('users.urls', namespace='users')),
    
]
