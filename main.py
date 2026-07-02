import os
import base64
import gspread
from google.oauth2.service_account import Credentials

print("===== BOT STARTED =====")

# Decode credentials
credentials_b64 = os.getenv("GOOGLE_CREDENTIALS")

with open("credentials.json", "wb") as f:
    f.write(base64.b64decode(credentials_b64))

print("Credentials तयार झाले.")

# Google Auth
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

print("Google Login Success")

# इथे तुझा Spreadsheet ID टाक
SPREADSHEET_ID = "PASTE_YOUR_SPREADSHEET_ID_HERE"

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

print("Spreadsheet Open Success")

rows = sheet.get_all_records()

print(f"Total Rows : {len(rows)}")

print("===== SUCCESS =====")
