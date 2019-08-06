
#python setup.py install
import tweepy
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import pynance
import os

cwd = os.getcwd()

search_term = input("Enter search term: ")

# Consumer keys and access tokens, used for OAuth
consumer_key = 'w63C4atArEWi9KE1ee9NtLgQw'
consumer_secret = 'izmhkAR15QL3o3esVPZIasqLXUX485kWPmEN6UmUdHOj8rKrNy'
access_token = '930535545918324736-LpC3If3mhmpPRmskxhXtcNG7Zd194Cg'
access_token_secret = 'MBvOE88jsYpCmxtUxcxPLfRWVaCWggC1mxSmO6DU8Qeh9'
 
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
