from transformers import pipeline
import pandas as pd
import praw
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup Hugging Face pipelines
threat_classifier = pipeline("text-classification", model="unitary/unbiased-toxic-roberta", top_k=None)
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Attributes to check from threat classifier
THREAT_LABELS = ["TOXIC", "SEVERE_TOXICITY", "INSULT", "THREAT", "IDENTITY_ATTACK"]

# =======================
# Helper functions
# =======================

def clean_text(text):
    return text.replace("\n", " ").lower()

def infer_severity(score):
    if score >= 0.85:
        return "High"
    elif score >= 0.5:
        return "Moderate"
    else:
        return "Low"

def get_ip_section(location):
    # Simulated or stub IP section
    return "UNKNOWN" if not location else f"{location[:3].upper()}-SECTION"

# =======================
# Load Tweets from File
# =======================
with open("../data/tweets.json", "r", encoding="utf-8") as file:
    tweets_data = [json.loads(line) for line in file]

twitter_df = pd.DataFrame(tweets_data)
twitter_df["platform"] = "Twitter"
twitter_df["user_id"] = twitter_df["user"].apply(lambda u: u.get("id_str", "UNKNOWN"))
twitter_df["location"] = twitter_df["user"].apply(lambda u: u.get("location", "UNKNOWN"))

# =======================
# Fetch Reddit Posts
# =======================
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="threat-monitor-script"
)

subreddit = reddit.subreddit("news")  # Change to any
reddit_data = []

for submission in subreddit.hot(limit=20):
    if submission.selftext:
        reddit_data.append({
            "text": submission.title + " " + submission.selftext,
            "user_id": submission.author.name if submission.author else "UNKNOWN",
            "platform": "Reddit",
            "location": "UNKNOWN"
        })

reddit_df = pd.DataFrame(reddit_data)

# =======================
# Combine All Data
# =======================
df = pd.concat([twitter_df[["text", "user_id", "location", "platform"]], reddit_df], ignore_index=True)

# =======================
# Analyze
# =======================
results = []

for _, row in df.iterrows():
    text = clean_text(row["text"])
    threat_preds = threat_classifier(text)[0]
    sentiment = sentiment_analyzer(text)[0]

    threat_scores = {item["label"]: item["score"] for item in threat_preds}
    top_label = max(threat_scores, key=threat_scores.get)
    top_score = threat_scores[top_label]
    severity = infer_severity(top_score)

    results.append({
        "Platform": row["platform"],
        "User ID": row["user_id"],
        "Text": text,
        "Threat Type": top_label,
        "Threat Score": round(top_score, 3),
        "Severity": severity,
        "Sentiment": sentiment["label"],
        "IP Section": get_ip_section(row["location"])
    })

# =======================
# Save Output
# =======================
result_df = pd.DataFrame(results)
result_df.to_csv("../data/classified_combined_output.csv", index=False)

print("✅ HuggingFace-based threat classification complete. Output saved.")
