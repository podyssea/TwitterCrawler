# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:26:33 2021

@author: odyss
"""

import os
import time
import tweepy

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
