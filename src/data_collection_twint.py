import twint
import pandas as pd

# --- Hashtag Query ---
hashtags = ["#Solana", "#Sol", "#Solprice", "#Soltrade", "#Solnft"]

# --- Combined results ---
all_tweets = []

# --- Loop through each hashtag separately (Twint does not support complex OR queries well) ---
for hashtag in hashtags:
    c = twint.Config()
    c.Search = hashtag
    c.Limit = 10  # You can increase this
    c.Lang = "en"
    c.Pandas = True
    c.Hide_output = True  # Optional: prevent printing to console

    # Run the search
    twint.run.Search(c)

    # Fetch DataFrame and append
    tweets_df = twint.storage.panda.Tweets_df

    if not tweets_df.empty:
        all_tweets.append(tweets_df)

# --- Combine and clean ---
if all_tweets:
    df = pd.concat(all_tweets, ignore_index=True)

    # Drop duplicate tweets by ID
    df.drop_duplicates(subset="id", inplace=True)

    # Optional: Select and rename columns to match snscrape version
    df = df[[
        "date", "id", "tweet", "username", "name", "verified",
        "followers", "likes_count", "retweets_count", "replies_count",
        "quote_url", "hashtags", "source", "language", "link"
    ]].rename(columns={
        "tweet": "content",
        "name": "user_displayname",
        "verified": "user_verified",
        "followers": "user_followers",
        "likes_count": "like_count",
        "retweets_count": "retweet_count",
        "replies_count": "reply_count",
        "quote_url": "quote_count",  # Twint does not return quote count directly
        "language": "lang",
        "link": "url"
    })

    # Save to CSV
    df.to_csv("solana_related_tweets_twint.csv", index=False)
    print(f"Scraped {len(df)} unique tweets using Twint.")
else:
    print("No tweets found.")
