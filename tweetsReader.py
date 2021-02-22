# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:36:31 2021

@author: odyss
"""

from mongoengine import DoesNotExist

from source.get_tweets import get_clean_tweets
from source.database_classes import connect_to_mongo, Tweet, ProcessedTweet

connect_to_mongo()

# for tweet in Tweet.objects.limit(10):
#     unwrapped_text = tweet.text.replace('\n', '\t')
#     print(f"{tweet.id_str} [{tweet.emotion_label}]: {unwrapped_text}")

for tweet in ProcessedTweet.objects(emotion_label="fear").limit(50):
    unwrapped_text = tweet.processed_text.replace('\n', '\t')
    print(f"{tweet.id_str} [{tweet.emotion_label}]: {unwrapped_text}")

print(f"{Tweet.objects.count()} Tweets stored in DB")
print(f"{ProcessedTweet.objects.count()} Processed Tweets stored in DB")