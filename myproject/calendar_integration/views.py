from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import pytz
import subprocess
import os


def get_google_creds():
    cred_file = 'C:/Users/Gabriel/Desktop/API_GoogleCalendar/myproject/token.json'
    creds = None
    if os.path.exists(cred_file):
        creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/calendar'])

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        subprocess.run(['python', 'C:/Users/Gabriel/Desktop/API_GoogleCalendar/myproject/generate_token.py'])
        creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/calendar'])

    return creds


@api_view(['GET'])
def get_events(request):
    if request.method == 'GET':
        try:
            creds = get_google_creds()
            print(f'Creds token: {creds.token}')
            service = build('calendar', 'v3', credentials=creds)
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(
                calendarId='primary', timeMin=now, singleEvents=True,
                orderBy='startTime').execute()
            events_data = events_result.get('items', [])

            return Response(events_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
