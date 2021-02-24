# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:38:02 2021

@author: odysseas polycarpou
"""

from dateutil.parser import parse as date_parse
from mongoengine import DoesNotExist, NotUniqueError
import tweepy

from source.get_tweets import get_clean_tweets
from source.database_classes import connect_to_mongo, Tweet
from source.sentiments import EMOTION_CLASS_MAP

NUM_CLEAN_TWEETS_PER_CLASS = 150


def do_save_tweets():
    connect_to_mongo()
    tweets_by_emotion = get_clean_tweets(
        EMOTION_CLASS_MAP,
        NUM_CLEAN_TWEETS_PER_CLASS
    )

    for emotion, tweets in tweets_by_emotion.items():
        for tweet in tweets:
            print(tweet.get("id_str"))
            try:
                tweet_model = Tweet.objects(id_str=tweet.get("id_str")).get()
            except DoesNotExist:
                tweet_model = Tweet(id_str=tweet.get("id_str"))

            tweet_model.text = tweet.get("text")
            tweet_model.emotion_label = emotion
            tweet_model.created_at = date_parse(tweet.get("created_at"))

            # ensure no duplicates end up in the dataset
            try:
                tweet_model.save()
            except NotUniqueError:
                print(f"Tweet {tweet_model.id_str} not unique - not persisting...")


if __name__ == "__main__":
    do_save_tweets()
