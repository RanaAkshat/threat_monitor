from transformers import pipeline
import pandas as pd
import json

# =======================
# Load tweets from JSON (Handle multiple objects line-by-line)
# =======================
tweets_data = []
with open("data/tweets.json", "r", encoding="utf-8") as file:
    for line in file:
        tweets_data.append(json.loads(line))

# Convert to DataFrame
df = pd.DataFrame(tweets_data)
print(df.columns)
print(df.head())


# =======================
# Load classification pipeline
# =======================
classifier = pipeline("text-classification", model="unitary/unbiased-toxic-roberta", top_k=None)

# Preprocessing function (basic)
def clean_text(text):
    text = text.replace("\n", " ")
    text = text.lower()
    return text

# =======================
# Classify the tweets
# =======================
results = []
for text in df["text"]:  
    cleaned = clean_text(text)
    prediction = classifier(cleaned)
    results.append(prediction)

# Flatten results into readable format
processed_results = []
for tweet, prediction in zip(df["text"], results): 
    tags = {item['label']: item['score'] for item in prediction[0]}
    processed_results.append({
        "Tweet": tweet,
        **tags
    })

# =======================
# Save Output to CSV
# =======================
result_df = pd.DataFrame(processed_results)
result_df.to_csv("data/classified_tweets.csv", index=False)

print("✅ NLP threat classification completed. Output saved to 'data/classified_tweets.csv'")
