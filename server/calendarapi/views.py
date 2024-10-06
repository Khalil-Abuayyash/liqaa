import os
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from .models import Availability, Interview
from .serializers import AvailabilitySerializer, InterviewSerializer
from .google_calendar import create_event, list_events
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/cloud-platform',
]
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'credentials.json')

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def perform_create(self, serializer):
        interview = serializer.save()  
        event = create_event(
            summary=f"Interview: {interview.interviewer.username} with {interview.interviewee.username}",
            start_time=datetime.combine(interview.scheduled_date, interview.start_time),
            end_time=datetime.combine(interview.scheduled_date, interview.end_time)
        )

        if not event:
            logger.error("Could not create event in Google Calendar.")
            raise Exception("Could not create event in Google Calendar.")

def initiate_oauth(request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://127.0.0.1:8080/api/calendarapi/oauth2callback/'
    )
    
    authorization_url, state = flow.authorization_url(access_type='offline')
    logger.info(f"Generated state: {state}")  
    request.session['state'] = state  
    return redirect(authorization_url)

def oauth2callback(request):    
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://127.0.0.1:8080/api/calendarapi/oauth2callback/'
    )

    state = request.GET.get('state')
    logger.info(f"Received state: {state}")  
    logger.info(f"Stored state: {request.session.get('state')}")  
    if state != request.session.get('state'):
        return JsonResponse({"error": "Invalid state parameter."}, status=400)

    if 'error' in request.GET:
        return JsonResponse({"error": request.GET['error']}, status=400)

    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    creds = flow.credentials

    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')
    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())

    return HttpResponse("Authentication successful! Token has been generated and saved.")

@api_view(['POST'])
def create_event_view(request):
    interview_data = request.data
    serializer = InterviewSerializer(data=interview_data)

    if serializer.is_valid():
        interview = serializer.save()  

        event = create_event(
            summary=f"Interview: {interview.interviewer.username} with {interview.interviewee.username}",
            start_time=datetime.combine(interview.scheduled_date, interview.start_time),
            end_time=datetime.combine(interview.scheduled_date, interview.end_time)
        )

        if not event:
            return JsonResponse({"error": "Could not create event in Google Calendar."}, status=500)

        return JsonResponse({"success": "Interview created and event added successfully."}, status=201)

    return JsonResponse({"error": serializer.errors}, status=400)


def get_credentials(token_path):
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if creds and creds.valid:
            return creds
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return creds
    return None

@api_view(['GET'])
def list_events_view(request):
    try:
        token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')
        creds = get_credentials(token_path)

        if creds is None:
            return JsonResponse({"error": "No valid credentials found."}, status=401)

        events = list_events(credentials=creds)

        if events:
            return JsonResponse({"events": events})
        else:
            return JsonResponse({"message": "No upcoming events found."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
