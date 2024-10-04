from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

def create_event(summary, start_time, end_time):
    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calendarapi', 'token.json')
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(token_path)
    except Exception as e:
        print("Failed to load credentials:", e)
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
