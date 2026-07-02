import gspread
import datetime
import requests
import json
import base64
import os

# =======================
# ENV VARIABLES
# =======================
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_USERNAME = os.environ["CHANNEL_USERNAME"]

# =======================
# GOOGLE CREDENTIALS (BASE64 → JSON)
# =======================
with open("credentials.json", "wb") as f:
    f.write(base64.b64decode(os.environ["GOOGLE_CREDENTIALS"]))

gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Telegram Quiz Automation").sheet1

# =======================
# TODAY DATE
# =======================
today = datetime.date.today().strftime("%Y-%m-%d")

data = sheet.get_all_records()

# =======================
# FIND TODAY QUESTION
# =======================
for i, row in enumerate(data):

    if row["Date"] == today and row["Status"] != "Posted":

        question = row["Question"]

        options = [
            row["Option 1"],
            row["Option 2"],
            row["Option 3"],
            row["Option 4"]
        ]

        correct = int(row["Correct Option"]) - 1

        payload = {
            "chat_id": CHANNEL_USERNAME,
            "question": question,
            "options": json.dumps(options),
            "type": "quiz",
            "correct_option_id": correct,
            "is_anonymous": False
        }

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPoll"

        res = requests.post(url, data=payload)

        print(res.text)

        if res.status_code == 200:
            sheet.update_cell(i + 2, 12, "Posted")
