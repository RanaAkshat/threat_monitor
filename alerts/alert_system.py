import pandas as pd
import time
import os
from twilio.rest import Client

# Twilio config
ACCOUNT_SID = "AC230554cc64143ee1a9d9ea860027a555"
AUTH_TOKEN = "49dd837520f6b1d9fd51d2b6a62dbcf5"
FROM_WHATSAPP = "whatsapp:+14155238886"
TO_WHATSAPP = "whatsapp:+919310063601"

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
