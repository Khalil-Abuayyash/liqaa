import os
import json
from datetime import timedelta
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Availability, Interview
from .serializers import AvailabilitySerializer, InterviewSerializer
from .google_calendar import create_event
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from django.shortcuts import redirect

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/cloud-platform', 
]
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'credentials.json')
TOKEN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')

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
        start_time = interview['start_time']
        end_time = interview['end_time']

        event = create_event(
            summary=f"Interview: {interviewer.username} with {interviewee.username}",
            start_time=start_time,
            end_time=end_time,
            credentials=self.get_credentials()
        )
        
        if event is None:
            return Response({"error": "Could not create event in Google Calendar."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

    def get_credentials(self):
        """Helper method to get Google OAuth credentials"""
        creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'r') as token:
                creds = Credentials.from_authorized_user(json.load(token), SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Automatically refresh the token
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(creds.to_json())
        elif not creds:
            raise Exception("User needs to authenticate again. Please initiate OAuth flow.")

        return creds

def initiate_oauth(request):
    """Initiate OAuth 2.0 flow to get user consent"""
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/api/calendarapi/oauth2callback/'  # Updated redirect URI for local development
    )

    authorization_url, state = flow.authorization_url(access_type='offline')
    request.session['state'] = state  
    return redirect(authorization_url)

def oauth2callback(request):
    """Handle the OAuth callback and save the token"""
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/api/calendarapi/oauth2callback/'  # Updated redirect URI for local development
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials

    with open(TOKEN_PATH, 'w') as token_file:
        token_file.write(creds.to_json())

    return HttpResponse("Authentication successful! Token has been generated and saved.")
