import tweepy
import json

# Replace with your actual Bearer Token from Twitter Developer Portal
bearer_token = "AAAAAAAAAAAAAAAAAAAAABJC1AEAAAAAwmqwLL55h%2FBnI3br1%2FDx1lvZqV0%3DLD9Pzpt2mideqyKTpNllcpTYN4qecNTbR0hY70IhRsjzvBoGm3"

# Set up Tweepy client with bearer token
client = tweepy.Client(bearer_token=bearer_token)

# Search for recent tweets using Twitter API v2
query = "#AI -is:retweet lang:en"  # example query: #AI, not retweets, in English
tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["created_at", "text", "author_id"])

# Save tweets to a file
with open("data/tweets.json", "w", encoding="utf-8") as f:
    for tweet in tweets.data:
        json.dump(tweet.data, f)
        f.write("\n")

print("Fetched and saved tweets using API v2.")
