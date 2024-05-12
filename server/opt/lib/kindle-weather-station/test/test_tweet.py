#!/usr/bin/env python3
# encoding=utf-8
# -*- coding: utf-8 -*-

import re
from twikit import Client
import json
from deep_translator import GoogleTranslator
#import pandas as pd

settings = 'settings_twitter.json'
with open(settings, 'r') as f:
    service = json.load(f)['station']
    twitter = service['twitter']
    screen_name = twitter['screen_name']

twitter_config = 'twitter_config.json'
with open(twitter_config, 'r') as f:
    t = json.load(f)['twitter']
    user =  t["user_screen_name"]
    password =  t["password"]

client = Client('en-US')
client.login(auth_info_1=user, password=password)
client.save_cookies('cookies.json')
client.load_cookies(path='cookies.json')
user = client.get_user_by_screen_name(screen_name)
tweets = user.get_tweets('Tweets', count=1)

tweets_to_store = []
for tweet in tweets:
    tweets_to_store.append({
        'created_at': tweet.created_at,
        'favorite_count': tweet.favorite_count,
        'full_text': tweet.full_text,
    })

#df = pd.DataFrame(tweets_to_store)
#df.to_csv('tweets.csv', index=False)
#a = df.sort_values(by='favorite_count', ascending=False)

pattern = r'http[s]*\S+'
urls = re.findall(pattern, tweets_to_store[0]['full_text'])
full_text = re.sub(pattern, '', tweets_to_store[0]['full_text'])
print('original:', tweets_to_store[0])
print('urls:', urls)
print('full_text(orig):', full_text)
translated = GoogleTranslator(source='auto', target='en').translate(full_text)
print('translate:', translated)
