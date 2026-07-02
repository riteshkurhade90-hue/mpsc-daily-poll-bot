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
import requests
import json

# पहिली Row घे
row = rows[0]

question = row["Question"]

options = [
    row["Option 1"],
    row["Option 2"],
    row["Option 3"],
    row["Option 4"]
]

correct_option = int(row["Correct Option"]) - 1

url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendPoll"

payload = {
    "chat_id": os.environ["CHANNEL_USERNAME"],
    "question": question,
    "options": json.dumps(options, ensure_ascii=False),
    "type": "quiz",
    "correct_option_id": correct_option,
    "is_anonymous": True,
    "explanation": row["Explanation"]
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.text)
