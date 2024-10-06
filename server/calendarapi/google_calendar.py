import os
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

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
        print("Error creating event:", e)
        return None

def list_events(credentials):
    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events
    except Exception as e:
        print("Error listing events:", e)
        return None

def get_credentials(token_path):
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(token_path)
    except Exception as e:
        print("Failed to load credentials:", e)
        return None

    return creds
