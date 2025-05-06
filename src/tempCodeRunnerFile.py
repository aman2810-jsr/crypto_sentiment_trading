import snscrape.modules.twitter as sntwitter
import pandas as pd

# --- Hashtag Query ---
hashtags = ["#Solana", "#Sol", "#Solprice", "#Soltrade", "#Solnft"]
query = "(" + " OR ".join(hashtags) + ") lang:en"

# --- Scraping Parameters ---
max_tweets = 10 # You can increase this
tweets = []

# --- Scraping Loop ---
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= max_tweets:
        break
    tweets.append({
        'date': tweet.date,
        'id': tweet.id,
        'content': tweet.content,
        'username': tweet.user.username,
        'user_displayname': tweet.user.displayname,
        'user_verified': tweet.user.verified,
        'user_followers': tweet.user.followersCount,
        'like_count': tweet.likeCount,
        'retweet_count': tweet.retweetCount,
        'reply_count': tweet.replyCount,
        'quote_count': tweet.quoteCount,
        'hashtags': tweet.hashtags,
        'source': tweet.sourceLabel,
        'lang': tweet.lang,
        'url': tweet.url,
    })

# --- Save to DataFrame ---
df = pd.DataFrame(tweets)

# --- Drop Duplicates by Tweet ID (to handle repeated hashtags) ---
df.drop_duplicates(subset='id', inplace=True)

# --- Save to CSV ---
df.to_csv("solana_related_tweets.csv", index=False)

print(f"Scraped {len(df)} unique tweets.")
