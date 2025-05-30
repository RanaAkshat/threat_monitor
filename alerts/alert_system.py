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

# Print ENV variables for debugging
print("🧪 ENV loaded:")
print("FROM_WHATSAPP:", FROM_WHATSAPP)
print("TO_WHATSAPP:", TO_WHATSAPP)
print("ACCOUNT_SID:", ACCOUNT_SID[:6], "...")  # Show only part of SID

client = Client(ACCOUNT_SID, AUTH_TOKEN)

FILE_PATH = "../data/categorized_tweets.csv"
SEEN_IDS = set()

def send_whatsapp_alert(threat, tweet):
    message_body = f"🚨 {threat}\nTweet: {tweet}"
    try:
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP,
            body=message_body
        )
        print(f"📲 WhatsApp alert sent! SID: {message.sid}")
    except Exception as e:
        print("❌ Failed to send WhatsApp message:", e)

def monitor_file():
    print("📡 Real-time threat monitor with WhatsApp alerts started...")

    while True:
        if os.path.exists(FILE_PATH):
            print("✅ File found!")
            try:
                df = pd.read_csv(FILE_PATH)
                print(f"📄 {len(df)} rows loaded from CSV.")
            except Exception as e:
                print("❌ Error reading CSV file:", e)
                continue

            for i, row in df.iterrows():
                tweet = row.get("Tweet", "")
                threat = row.get("Threat_Category", "")
                tweet_id = hash(tweet)

                if tweet_id in SEEN_IDS:
                    continue

                print(f"🔍 Checking tweet: {tweet}")
                print(f"🛑 Threat category: {threat}")

                if "Critical" in threat or "High" in threat:
                    print(f"🚨 ALERT! {threat}\n🗣️ {tweet}\n")
                    send_whatsapp_alert(threat, tweet)

                SEEN_IDS.add(tweet_id)
        else:
            print("⚠️ Waiting for file:", FILE_PATH)

        time.sleep(5)

if __name__ == "__main__":
    monitor_file()
