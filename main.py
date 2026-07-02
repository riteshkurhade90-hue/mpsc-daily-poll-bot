import os
import json
import time
import base64
import requests
import gspread

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
# Current Day
# ===========================

CURRENT_DAY = int(time.strftime("%d"))

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

📝 एकूण प्रश्न: 25

⏱️ सर्व प्रश्न काळजीपूर्वक सोडवा.

सर्वांना मनःपूर्वक शुभेच्छा! 💐
""")# ===========================
# Send Today's Quiz Polls
# ===========================

posted_count = 0

for row in rows:

    # फक्त आजच्या Day चे प्रश्न
    if int(row["Day"]) != CURRENT_DAY:
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

    time.sleep(2)


# ===========================
# End Message
# ===========================

if posted_count > 0:

    send_message(f"""✅ आजची Day {CURRENT_DAY} टेस्ट पूर्ण झाली.

सहभागासाठी धन्यवाद! 🙏

📖 उद्या दुपारी ३:०० वाजता पुढील विषयावर नवीन टेस्ट उपलब्ध होईल.

अभ्यास करत रहा आणि नियमित सराव करा. 💪
""")

else:

    send_message(f"⚠️ Day {CURRENT_DAY} साठी कोणतेही प्रश्न उपलब्ध नाहीत.")

print("===== BOT FINISHED SUCCESSFULLY =====")
