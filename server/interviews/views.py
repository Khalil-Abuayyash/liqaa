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
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        user_id = request.data.get('user')
        available_date = request.data.get('available_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
 
        if end_time <= start_time:
            return Response({'status': 'conflict', 'message': 'End time must be after start time.'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='not booked'
        )

        existing_availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__gt=start_time,
            end_time__lt=end_time,
            status='not booked'
        ).first()

        if existing_availability:
            existing_availability.start_time = start_time
            existing_availability.end_time = end_time
            existing_availability.save()
            return Response({'status': 'updating', 'message': 'The availability has been modified.'}, status=status.HTTP_200_OK)

        booked_availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='booked'
        )
        
       
        if booked_availability.exists(): 
            if booked_availability <= start_time and booked_availability >= end_time: 
                booked_availability.delete() 
            
            elif booked_availability <= start_time and booked_availability <= end_time: 
                booked_availability.delete() 
                
            elif booked_availability >= start_time and booked_availability <= end_time:
                booked_availability.delete() 
            
            elif booked_availability >= start_time and booked_availability >= end_time: 
                booked_availability.delete()
    
        else: 
            response = super().create(request, *args, **kwargs)
            return Response({'status': 'creating', 'message': 'New availabilities were created before and after the existing booked slot.'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'created', 'message': 'Availability created successfully.', 'data': response.data}, status=status.HTTP_201_CREATED)
    
     
    
class InterviewViewSet(viewsets.ModelViewSet): 
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    
    def create(self, request, *args, **kwargs): 
        pass
    
    


