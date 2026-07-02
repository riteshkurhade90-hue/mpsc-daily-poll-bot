import os
import time
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
def send_message(text):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"

    payload = {
        "chat_id": os.environ["CHANNEL_USERNAME"],
        "text": text
    }

    requests.post(url, json=payload)
start_message = """📚 MPSC Daily Quiz | Day 3

🎯 आजची नागरिकत्व (Citizenship) टेस्ट सुरू झाली आहे.

📝 एकूण प्रश्न: 25
⏱️ सर्व प्रश्न काळजीपूर्वक सोडवा.

सर्वांना मनःपूर्वक शुभेच्छा! 💐"""

send_message(start_message)
# पहिली Row घे
for row_number, row in enumerate(rows, start=2):
if row["Status"] == "Posted":
    continue
    question = row["Question"]

    options = [
        row["Option 1"],
        row["Option 2"],
        row["Option 3"],
        row["Option 4"]
    ]

    correct_option = int(row["Correct Option"]) - 1

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

    time.sleep(2)

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
if response.status_code == 200:
    sheet.update_cell(row_number, 11, "Posted")
end_message = """✅ आजची Day 3 टेस्ट पूर्ण झाली.

सहभागासाठी धन्यवाद! 🙏

📖 उद्या दुपारी ३:०० वाजता पुढील विषयावर नवीन टेस्ट उपलब्ध होईल.

अभ्यास करत रहा आणि नियमित सराव करा. 💪"""

send_message(end_message)
