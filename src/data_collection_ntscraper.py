import random
import pandas as pd
from ntscraper import Nitter

# Initialize the scraper
nitter_instances = [
    "https://nitter.net",
    "https://nitter.42l.fr",
    "https://nitter.mstdn.social"
]

# Pick a random instance to try
scraper = Nitter(random.choice(nitter_instances))

# Define the hashtags to search for
hashtags = ["#Solana", "#Sol", "#Solprice", "#Soltrade", "#Solnft"]
max_tweets = 10  # Number of tweets to fetch per hashtag

# List to store all tweets
all_tweets = []

# Loop through each hashtag
for tag in hashtags:
    # Fetch tweets for the current hashtag
    tweets_data = scraper.get_tweets(tag, mode='hashtag', number=max_tweets)
    
    # Check if tweets are returned
    if tweets_data and 'tweets' in tweets_data:
        for tweet in tweets_data['tweets']:
            all_tweets.append({
                'date': tweet.get('date'),
                'id': tweet.get('id'),
                'content': tweet.get('text'),
                'username': tweet.get('username'),
                'user_displayname': tweet.get('name'),
                'user_verified': tweet.get('verified'),
                'user_followers': tweet.get('followers'),
                'like_count': tweet.get('likes'),
                'retweet_count': tweet.get('retweets'),
                'reply_count': tweet.get('replies'),
                'quote_count': tweet.get('quotes'),
                'hashtags': tweet.get('hashtags'),
                'source': tweet.get('source'),
                'lang': tweet.get('lang'),
                'url': tweet.get('link'),
            })

# Create a DataFrame from the list of tweets
df = pd.DataFrame(all_tweets)

# Drop duplicate tweets based on the 'id' field
df.drop_duplicates(subset='id', inplace=True)

# Save the DataFrame to a CSV file
df.to_csv("solana_related_tweets_ntscraper.csv", index=False)

print(f"Scraped {len(df)} unique tweets using ntscraper.")
