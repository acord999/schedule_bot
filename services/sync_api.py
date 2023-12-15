import pprint
import sys

from config_data.config import load_config
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

COLORS_CATEGORIES = {
    # key - category id from db; data - color id by Google
    1: 9,
    2: 5,
    3: 11
}

settings = load_config().google_calendar


class GoogleCalendar:
    ACCOUNT_INFO = settings.filepath
    SCOPES = [settings.scopes]

    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        credentials = service_account.Credentials.from_service_account_file(filename=self.ACCOUNT_INFO,
                                                                            scopes=self.SCOPES)
        self.service = build("calendar", "v3", credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }

        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, title, time_start, time_stop, category=8, location=None, description=None):
        event = {
            'summary': f'{title}',
            'location': f'{location}',
            'description': f'{description}',
            'start': {
                'dateTime': time_start.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'dateTime': time_stop.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                ],
            },
            "colorId": COLORS_CATEGORIES.get(category, 8)
        }
        return self.service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def get_events(self):
        page_token = None
        while True:
            events = self.service.events().list(calendarId=self.calendar_id, pageToken=page_token).execute()
            for event in events['items']:
                pprint.pprint(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break


if __name__ == "__main__":
    t1 = datetime.datetime(2023, 10, 31, 8, 0)
    t2 = datetime.datetime(2023, 10, 31, 9, 0)
    obj = GoogleCalendar(
        "ea37c3a01ef11bae5544b5a0061d4953afb60cb84e25392e8ab982571d0657e4@group.calendar.google.com")
    obj.add_event("dhfjdshgjdf", time_start=t1, time_stop=t2)
