import os
from datetime import timedelta
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Availability, Interview
from .serializers import AvailabilitySerializer, InterviewSerializer
from .google_calendar import create_event  # Assuming this exists in 'google_calendar.py'
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'credentials.json')

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def perform_create(self, serializer):
        interview = serializer.validated_data
        
        interviewer = interview['interviewer']
        interviewee = interview['interviewee']
        interviewer_availability = interview['interviewer_availability']
        interviewee_availability = interview['interviewee_availability']
        start_time = interview['start_time']
        end_time = interview['end_time']

        # Create a calendar event when the interview is created
        event = create_event(
            summary=f"Interview: {interviewer.username} with {interviewee.username}",
            start_time=start_time,
            end_time=end_time
        )
        
        if event is None:
            return Response({"error": "Could not create event in Google Calendar."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

def initiate_oauth(request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://0286-194-169-121-112.ngrok-free.app/api/calendarapi/oauth2callback/'
    )

    authorization_url, state = flow.authorization_url(access_type='offline')
    request.session['state'] = state  
    return redirect(authorization_url)

def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://0286-194-169-121-112.ngrok-free.app/api/calendarapi/oauth2callback/'
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials

    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    return HttpResponse("Authentication successful! You can close this window.")
