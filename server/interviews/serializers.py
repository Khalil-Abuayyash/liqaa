from rest_framework import serializers
from .models import Availability, Interview

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'user', 'available_date', 'start_time', 'end_time', 'status']

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'interviewer', 'interviewee', 'interviewer_availability', 'interviewee_availability', 'scheduled_date', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
