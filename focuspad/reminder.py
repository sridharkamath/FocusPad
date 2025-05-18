import os, schedule, threading, time
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()  # loads .env at project root

def _send_sms():
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
    )
    client.messages.create(
        body=f"FocusPad ⏰  {datetime.now():%H:%M} — time to journal!",
        from_="+15017122661",           # your Twilio number
        to=os.getenv("MY_PHONE_NUMBER"),
    )

def schedule_reminder():
    schedule.every().day.at("21:00").do(_send_sms)

    def runner():
        while True:
            schedule.run_pending()
            time.sleep(30)

    threading.Thread(target=runner, daemon=True).start()
