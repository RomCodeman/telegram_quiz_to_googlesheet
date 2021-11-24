from os import getenv, environ
from pathlib import Path

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from telebot import TeleBot

from telegram_quiz_to_googlesheet.settings.base import BASE_DIR

dotenv_path = Path(f'{BASE_DIR}/.env')
load_dotenv(dotenv_path=dotenv_path)

# Telegram Bot definition

TOKEN = getenv("BOT2_TOKEN", "error_token")

bot: TeleBot = TeleBot(TOKEN)


# Google Sheets definitions

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

SHEETS_CREDENTIALS = {
    "type": "service_account",
    "project_id": environ["GOOGLE_SHEET_PROJECT_ID"],
    "private_key_id": environ["GOOGLE_SHEET_PRIVATE_KEY_ID"],
    # Newline replacement still does not work properly. Must be set manually.
    "private_key": environ["GOOGLE_SHEET_PRIVATE_KEY"].replace(r'\n', '\n'),
    "client_email": environ["GOOGLE_SHEET_CLIENT_EMAIL"],
    "client_id": environ["GOOGLE_SHEET_CLIENT_ID"],
    "auth_uri": environ["GOOGLE_SHEET_AUTH_URI"],
    "token_uri": environ["GOOGLE_SHEET_TOKEN_URI"],
    "auth_provider_x509_cert_url": environ["GOOGLE_SHEET_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": environ["GOOGLE_SHEET_CLIENT_X509_CERT_URL"]
}

credentials: gspread.auth.ServiceAccountCredentials = ServiceAccountCredentials.from_json_keyfile_dict(SHEETS_CREDENTIALS, scope)

client_gspread: gspread.client = gspread.authorize(credentials)
