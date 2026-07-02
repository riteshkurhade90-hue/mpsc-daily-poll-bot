import os
import base64

print("===== BOT STARTED =====")

credentials = os.getenv("GOOGLE_CREDENTIALS")

if credentials is None:
    raise Exception("GOOGLE_CREDENTIALS Secret सापडला नाही.")

print("Secret मिळाला.")

decoded = base64.b64decode(credentials)

with open("credentials.json", "wb") as f:
    f.write(decoded)

print("credentials.json तयार झाली.")
print("===== SUCCESS =====")
