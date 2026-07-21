import os
import json
import time
import base64
import requests
import gspread

from datetime import datetime
from google.oauth2.service_account import Credentials

print("===== MPSC Daily Quiz Bot Started =====")

# ===========================
# Google Credentials
# ===========================

credentials = base64.b64decode(os.environ["GOOGLE_CREDENTIALS"])

with open("credentials.json", "wb") as f:
    f.write(credentials)

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

SPREADSHEET_ID = "1zR3ArmRBUhkomcd3rlJXeVKu0TrEvHC8zlqWflbJnds"

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

rows = sheet.get_all_records()

print(f"Total Rows : {len(rows)}")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["CHANNEL_USERNAME"]

# ===========================
# Automatic Day Detection
# ===========================

START_DATE = datetime(2026, 7, 22)

today = datetime.now()

CURRENT_DAY = (today - START_DATE).days + 1

if CURRENT_DAY < 1:
    CURRENT_DAY = 1

print(f"Today's Day : {CURRENT_DAY}")

# ===========================
# Telegram Functions
# ===========================

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=payload)

    print(response.text)


def send_poll(question, options, correct_option, explanation):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

    payload = {

        "chat_id": CHAT_ID,
        "question": question,
        "options": json.dumps(options, ensure_ascii=False),
        "type": "quiz",
        "correct_option_id": correct_option,
        "is_anonymous": True,
        "explanation": explanation

    }

    return requests.post(url, json=payload)

# ===========================
# Start Message
# ===========================

send_message(f"""📚 MPSC Daily Quiz | Day {CURRENT_DAY}

🎯 आजची टेस्ट सुरू झाली आहे.
🏆 विषय : इतिहास (आधुनिक)
📝 एकूण प्रश्न: 10

⏱️ सर्व प्रश्न काळजीपूर्वक सोडवा.

सर्वांना मनःपूर्वक शुभेच्छा! 💐
""")
# ===========================
# Send Today's Quiz Polls
# ===========================

posted_count = 0

for index, row in enumerate(rows):

    # फक्त आजच्या Day चे प्रश्न
    if int(row["Day"]) != CURRENT_DAY:
        continue

    # आधीच पोस्ट झाले असल्यास Skip
    status = str(row.get("Status", "")).strip().lower()

    if status == "posted":
        continue

    question = row["Question"]

    options = [
        row["Option 1"],
        row["Option 2"],
        row["Option 3"],
        row["Option 4"]
    ]

    correct_option = int(row["Correct Option"]) - 1

    explanation = row["Explanation"]

    response = send_poll(
        question,
        options,
        correct_option,
        explanation
    )

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:

        posted_count += 1

        # Status = Posted
        sheet.update_cell(index + 2, 10, "Posted")

    time.sleep(2)

    # फक्त 10 प्रश्न पाठवायचे
    if posted_count >= 10:
        break


# ===========================
# End Message
# ===========================

if posted_count > 0:

    send_message(f"""✅ आजची Day {CURRENT_DAY} टेस्ट पूर्ण झाली.

सहभागासाठी धन्यवाद! 🙏

📖 उद्या पुढील विषयावर नवीन टेस्ट उपलब्ध होईल.

अभ्यास करत रहा आणि नियमित सराव करा. 💪
""")

else:

    send_message(f"⚠️ Day {CURRENT_DAY} साठी पोस्ट करण्यासाठी नवीन प्रश्न उपलब्ध नाहीत.")

print("===== BOT FINISHED SUCCESSFULLY =====")
