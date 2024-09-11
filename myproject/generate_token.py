from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.conf import settings
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Scopes required for accessing Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    # Check if token file exists
    token_path = settings.GOOGLE_TOKEN_FILE
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path)
        except Exception as e:
            print(f"Error loading token: {e}")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Use the fixed port 8000
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    main()

