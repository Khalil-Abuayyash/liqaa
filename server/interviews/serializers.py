from rest_framework import serializers
from .models import Availability, Interview 

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'user', 'available_date', 'start_time', 'end_time']  

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'interviewer', 'scheduled_date', 'start_time', 'end_time', 'status']  