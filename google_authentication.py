"""Google authentication file."""

import gspread
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle


# Define the scopes required for accessing Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']


def authenticate_user() -> gspread.Client:
    """Authenticate the user via OAuth 2.0 and return a gspread client.

    This function checks for existing credentials stored in the `token.pickle` file.
    If not found, it initiates the OAuth 2.0 flow to authenticate the user and
    save the credentials for future use.

    Returns:
        gspread.Client: Authenticated gspread client for interacting with Google Sheets.
    """
    creds = None

    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are found, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'D:\pooja_project\credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the user's credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Authenticate with gspread using the credentials
    return gspread.authorize(creds)