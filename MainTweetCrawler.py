# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:38:02 2021

@author: odysseas polycarpou
"""

from dateutil.parser import parse as date_parse
from mongoengine import DoesNotExist, NotUniqueError
from source.tweetStreamer import get_clean_tweets
from source.database_classes import connect_to_mongo, Tweet
from source.sentiments import EMOTION_CLASS_MAP

#set the number of tweets per class
NUM_CLEAN_TWEETS_PER_CLASS = 150


#function to fetch and save tweets. This function fetches only clean tweets
# and discards duplicates. Returns the tweet id on the console screen and a message if the tweet is duplicated
def save_tweets():
    connect_to_mongo()
    tweets_by_emotion = get_clean_tweets(
        EMOTION_CLASS_MAP,
        NUM_CLEAN_TWEETS_PER_CLASS
    )

    for emotion, tweets in tweets_by_emotion.items():
        for tweet in tweets:
            print("Fetched Tweet ID - " + tweet.get("id_str"))
            try:
                tweet_model = Tweet.objects(id_str=tweet.get("id_str")).get()
            except DoesNotExist:
                tweet_model = Tweet(id_str=tweet.get("id_str"))

            tweet_model.text = tweet.get("text")
            tweet_model.emotion_label = emotion
            tweet_model.created_at = date_parse(tweet.get("created_at"))

            # get rid of duplications
            try:
                tweet_model.save()
            except NotUniqueError:
                print(f"Tweet {tweet_model.id_str} alredy exists - will discard.......")


if __name__ == "__main__":
    save_tweets()
