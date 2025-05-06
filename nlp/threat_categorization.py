import pandas as pd

# Load classified tweet data
df = pd.read_csv("data/classified_tweets.csv")

def categorize_threat(row):
    # Threshold logic
    if row.get("TOXICITY", 0) > 0.8:
        return "Critical Threat - Hate Speech"
    elif row.get("THREAT", 0) > 0.7:
        return "High Threat - Violence/Threat"
    elif row.get("INSULT", 0) > 0.6:
        return "Moderate Threat - Cyberbullying"
    elif row.get("IDENTITY_ATTACK", 0) > 0.5:
        return "Targeted Threat - Discrimination"
    else:
        return "Low Threat - Safe"

# Apply to all rows
df["Threat_Category"] = df.apply(categorize_threat, axis=1)

# Save categorized results
df.to_csv("data/categorized_tweets.csv", index=False)
print("✅ Threat categorization complete. Output saved to 'data/categorized_tweets.csv'")
