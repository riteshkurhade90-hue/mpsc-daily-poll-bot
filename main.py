import gspread
import datetime
import requests
import json

# =======================
# CONFIG (fill later in GitHub Secrets)
# =======================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@YOUR_CHANNEL"

# =======================
# Google Sheets Auth
# =======================
gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Telegram Quiz Automation").sheet1

# =======================
# Get today's date
# =======================
today = datetime.date.today().strftime("%Y-%m-%d")

data = sheet.get_all_records()

for row in data:
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

        if res.status_code == 200:
            sheet.update_cell(data.index(row)+2, 12, "Posted")

        print(res.text)
