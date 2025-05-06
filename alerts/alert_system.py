from dotenv import load_dotenv
import os
import pandas as pd
import time
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


FILE_PATH = "data/categorized_tweets.csv"
SEEN_IDS = set()

def send_whatsapp_alert(threat, tweet):
    message_body = f"🚨 {threat}\nTweet: {tweet}"
    message = client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        body=message_body
    )
    print(f"📲 WhatsApp alert sent! SID: {message.sid}")

def monitor_file():
    print("📡 Real-time threat monitor with WhatsApp alerts started...")

    while True:
        if os.path.exists(FILE_PATH):
            df = pd.read_csv(FILE_PATH)

            for i, row in df.iterrows():
                tweet_id = hash(row["Tweet"])

                if tweet_id in SEEN_IDS:
                    continue

                threat = row["Threat_Category"]
                tweet = row["Tweet"]

                if "Critical" in threat or "High" in threat:
                    print(f"🚨 ALERT! {threat}\n🗣️ {tweet}\n")
                    send_whatsapp_alert(threat, tweet)

                SEEN_IDS.add(tweet_id)

        time.sleep(5)

if __name__ == "__main__":
    monitor_file()
