from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import subprocess
import os


def get_google_creds():
    cred_file = 'C:/Users/Gabriel/Desktop/API_Google_Calendar/myproject/token.json'
    creds = None
    if os.path.exists(cred_file):
        creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/calendar'])
    else:
        subprocess.run(['python', 'C:/Users/Gabriel/Desktop/API_Google_Calendar/myproject/generate_token.py'])
        creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/calendar'])

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


@api_view(['GET'])
def get_events(request):
    if request.method == 'GET':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(
                calendarId='primary', timeMin=now, singleEvents=True,
                orderBy='startTime').execute()

            events_data = events_result.get('items', [])
            events_resume = []

            for event in events_data:
                event_info = {
                    'summary': event.get('summary', 'No title'),
                    'description': event.get('description', 'No description'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'Anytime')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date', 'Undefined')),
                    'participants': [attendee.get('email') for attendee in event.get('attendees', [])],
                    'id': event.get('id')
                }
                events_resume.append(event_info)

            return Response(events_resume, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_event_by_id(request, id):
    if request.method == 'GET':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)
            
            event = service.events().get(calendarId='primary', eventId=id).execute()
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            return Response(event, status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_events_by_period(request, start, end):
    if request.method == 'GET':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            if not events_result:
                return Response(status=status.HTTP_404_NOT_FOUND)

            events = events_result.get('items', [])
            return Response(events, status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_events_by_summary(request, summary):
    if request.method == 'GET':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(
                calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            filtered_events = [event for event in events if summary.lower() in event.get('summary', '').lower()]
            
            if not filtered_events:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            return Response(filtered_events, status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_event(request):
    if request.method == 'POST':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)
            
            event = {
                'summary': request.data.get('summary'),
                'start': {
                    'dateTime': request.data.get('start_time'),
                    'timeZone': 'America/Fortaleza',
                },
                'end': {
                    'dateTime': request.data.get('end_time'),
                    'timeZone': 'America/Fortaleza',
                },
            }
            
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            return Response(created_event, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_event(request):
    if request.method == 'PUT':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)

            id = request.data.get('id')
            if not id:
                return Response({"error": "Event ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            event = service.events().get(calendarId='primary', eventId=id).execute()

            event['summary'] = request.data.get('summary', event['summary'])
            event['start']['dateTime'] = request.data.get('start_time', event['start']['dateTime'])
            event['end']['dateTime'] = request.data.get('end_time', event['end']['dateTime'])

            updated_event = service.events().update(calendarId='primary', eventId=id, body=event).execute()
            return Response(updated_event, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_event(request):
    if request.method == 'DELETE':
        try:
            creds = get_google_creds()
            service = build('calendar', 'v3', credentials=creds)

            id = request.data.get('id')
            if not id:
                return Response({"error": "Event with this ID not found"}, status=status.HTTP_404_NOT_FOUND)
            
            service.events().delete(calendarId='primary', eventId=id).execute()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
