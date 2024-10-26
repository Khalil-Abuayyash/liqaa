from django.shortcuts import render
from rest_framework import viewsets, status
from django.db.models import Q
from .models import Availability, Interview
from .serializers import AvailabilitySerializer, InterviewSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.http import HttpResponse



class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
         
class InterviewViewSet(viewsets.ModelViewSet): 
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    
    
    


