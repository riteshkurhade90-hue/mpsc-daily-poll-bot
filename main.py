import os
import base64
import gspread
from google.oauth2.service_account import Credentials

print("===== BOT STARTED =====")

# Decode Base64 Secret
credentials = base64.b64decode(os.environ["GOOGLE_CREDENTIALS"])

with open("credentials.json", "wb") as f:
    f.write(credentials)

print("Credentials तयार झाले.")

# Google Authentication
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

# Spreadsheet ID
SPREADSHEET_ID = "1zR3ArmRBUhkomcd3rlJXeVKu0TrEvHC8zlqWflbJnds"

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

print("Spreadsheet Open Success")

rows = sheet.get_all_records()

print(f"एकूण Rows : {len(rows)}")

for row in rows[:5]:
    print(row)

print("===== SUCCESS =====")
