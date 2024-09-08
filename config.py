import os
import pickle
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load konfigurasi dari file .env
load_dotenv('CONFIG.ENV')

# Ambil token bot dan konfigurasi lainnya dari variabel environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
INOUT_ID = os.getenv("INOUT_ID")
LIST_ID = os.getenv("LIST_ID")
RANGE_NAME = os.getenv("RANGE_NAME")
RANGE_INOUT = os.getenv("RANGE_INOUT")
RANGE_STOK = os.getenv("RANGE_STOK")
RANGE_LIST=os.getenv("RANGE_LIST")

# Konfigurasi untuk OAuth2
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Ganti 'credentials.json' dengan path ke file JSON kredensial OAuth2 Anda
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()