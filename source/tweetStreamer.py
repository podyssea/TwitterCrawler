# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:26:33 2021

@author: odyss
"""

import os
import time
import itertools

from dotenv import load_dotenv
from TwitterAPI import TwitterAPI, TwitterError


#===============Set your KEYS and TOKENS here==================#
CONSUMER_KEY = "RpC3PQVErJ6NwEqYAy85hDKam"
CONSUMER_KEY_SECRET = "bIdIR94Q1QShZ6jAzbTWYNFryxmsz8YRCE3ZHhg0BVFPKkMI0d"
ACCESS_TOKEN = "1361687926686507013-1IuVkNJGyy3TOThnQEFjRNPGLxjaYJ"
ACCESS_TOKEN_SECRET = "zR7FXlT392WwoeJNh3hagl2xHpftVjQvmn1WilcwyPGCs"
#==============================================================#

def connect_to_client():
    load_dotenv()

    client = TwitterAPI(CONSUMER_KEY,
                    CONSUMER_KEY_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)
    return client


def stream_tweets_matching_filter(query_expression, filter_function):
    api = connect_to_client()


    #Make iterations fault fault tolerant
    def _fault_tolerant_response_iter():
        query_params = {
            'track': query_expression,
            'language': "en",
        }

        while True:
            try:
                for item in api.request("statuses/filter", query_params).get_iterator():
                    if "disconnect" in item:
                        event = item['disconnect']
                        if event['code'] in [2,5,6,7]:
                            raise ValueError(event['reason'])
                        else:
                            break
                    yield item
            except TwitterError.TwitterRequestError as exception:
                if exception.status_code < 420:
                    raise
                elif exception.status_code in (420, 429):
                    print(f"Being rate-limited (Status code: {e.status_code})... backing off...")
                    time.sleep(5)
                else:
                    continue
            except TwitterError.TwitterConnectionError:
                # temporary interruption, re-try request
                continue

    response_iter = _fault_tolerant_response_iter()
    return filter(filter_function,response_iter)

#Filter bad tweets
def filter_bad_tweets(tweet, desired_emotion_class, match_terms_map):
    for emotion, match_terms in match_terms_map.items():
        if emotion == emotion:
            continue

        for term in match_terms:
            if term in tweet.text:
                return False

    return True

#Get clean tweets
def get_clean_tweets(match_terms_map, tweets_per_emotion_class):
    clean_tweets_by_emotion_class = {}

    for emotion_class, match_terms in match_terms_map.items():
        query_expr = ",".join(match_terms)

        def _filter_bad_tweets(tweet):
            return filter_bad_tweets(tweet, emotion_class, match_terms_map)

        stream = stream_tweets_matching_filter(query_expr, _filter_bad_tweets)
        clean_tweets = itertools.islice(stream, tweets_per_emotion_class)
        clean_tweets_by_emotion_class[emotion_class] = clean_tweets

    return clean_tweets_by_emotion_class
