import os
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponse 
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.shortcuts import render
from .google_calendar import *
from rest_framework.response import Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.settings.readonly	']
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

    
def initiate_oauth(request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://127.0.0.1:8080/api/calendarapi/oauth2callback/'
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    request.session['state'] = state
    print('I am the state from initiate_oauth:', state)
    return redirect(authorization_url)

def oauth2callback(request):
    print("Hi, I am oauth2callback function!")
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='https://127.0.0.1:8080/api/calendarapi/oauth2callback/'
    )
    print(flow)

    state = request.GET.get('state')
    session_state = request.session.get('state')
    print("State from Google:", state)
    print("State from session:", session_state)

    if state != session_state:
        return JsonResponse({"error": "Invalid state parameter."}, status=400)

    if 'error' in request.GET:
        return JsonResponse({"error": request.GET['error']}, status=400)

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials

    print(creds)
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
    print("Saving token at:", token_path)
    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())

    return HttpResponse("Authentication successful! Token has been generated and saved.")

