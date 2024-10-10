import os
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_credentials(token_path):
    creds = None
    try:
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
    except Exception as e:
        print("Failed to load or refresh credentials:", str(e))
        return None

    return creds


def create_event(summary, start_time, end_time):
    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')
    creds = get_credentials(token_path)

    if creds is None:
        print("No valid credentials available.")
        return None

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',  
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event
    except Exception as e:
        print("Error creating event:", str(e))
        return None

def create_availability(summary, start_time, end_time):
    event = create_event(summary, start_time, end_time)
    if event:
        print("Availability created successfully.")
    else:
        print("Failed to create availability.")


def list_events(credentials):
    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=7, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events
    except Exception as e:
        print("Error listing events:", str(e))
        return None


