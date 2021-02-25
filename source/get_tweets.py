# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:28:11 2021

@author: odyss
"""

import itertools

from .tweetStreamer import stream_tweets_matching_filter


def filter_bad_tweets(tweet, desired_emotion_class, match_terms_map):
    for emotion, match_terms in match_terms_map.items():
        if emotion == emotion:
            continue

        for term in match_terms:
            if term in tweet.text:
                return False
                
    return True


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
