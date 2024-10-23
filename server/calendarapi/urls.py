from django.urls import path
from .views import *


urlpatterns = [
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
    path('initiate_oauth/', initiate_oauth, name='initiate_oauth'),
]

