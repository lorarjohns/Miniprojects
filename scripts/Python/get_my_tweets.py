# A script written for a friend
# who needed a way to get tweets
# with sentiment data, to use
# for a time series analysis
# to predict stock price changes.

import tweepy
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import pynance
import os

cwd = os.getcwd()

search_term = input("Enter search term: ")

# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
# Sample method, used to update a status

sid = SentimentIntensityAnalyzer()


tweets = api.search(search_term, count=100)
df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
df['Sentiment'] = df['Tweets'].apply(lambda x: sid.polarity_scores(x))
df['Good_Bad'] = df['Sentiment'].apply(lambda x: x['compound'])


df.to_csv(cwd + f"/{search_term}")
print(df)
