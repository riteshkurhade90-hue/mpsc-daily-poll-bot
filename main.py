import gspread
import datetime
import requests
import json
import base64
import os
import time

# ENV
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_USERNAME = os.environ["CHANNEL_USERNAME"]

# Decode credentials
with open("credentials.json", "wb") as f:
    f.write(base64.b64decode(os.environ["GOOGLE_CREDENTIALS"]))

gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Telegram Quiz Automation").sheet1

# TODAY
today = datetime.date.today().strftime("%Y-%m-%d")

data = sheet.get_all_records()

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPoll"

# LOOP ALL 25 QUESTIONS
for i, row in enumerate(data):

    if row["Date"] == today and row["Status"] != "Posted":

        try:
            question = row["Question"]

            options = [
                row["Option 1"],
                row["Option 2"],
                row["Option 3"],
                row["Option 4"]
            ]

            payload = {
                "chat_id": CHANNEL_USERNAME,
                "question": question,
                "options": json.dumps(options),
                "type": "quiz",
                "correct_option_id": int(row["Correct Option"]) - 1,
                "is_anonymous": False
            }

            res = requests.post(url, data=payload)

            print("Posted:", question, res.status_code)

            if res.status_code == 200:
                sheet.update_cell(i + 2, 11, "Posted")

            time.sleep(2)  # IMPORTANT: Telegram safe delay

        except Exception as e:
            print("Error:", e)
