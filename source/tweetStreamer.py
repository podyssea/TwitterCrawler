# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:26:33 2021

@author: odyss
"""

import os
import time

from dotenv import load_dotenv
from TwitterAPI import TwitterAPI, TwitterError


def get_client():
    load_dotenv()
    return TwitterAPI(
        os.getenv("RpC3PQVErJ6NwEqYAy85hDKam"),
        os.getenv("bIdIR94Q1QShZ6jAzbTWYNFryxmsz8YRCE3ZHhg0BVFPKkMI0d"),
        os.getenv("1361687926686507013-1IuVkNJGyy3TOThnQEFjRNPGLxjaYJ"),
        os.getenv("zR7FXlT392WwoeJNh3hagl2xHpftVjQvmn1WilcwyPGCs"),
    )


def stream_tweets_matching_filter(query_expression, filter_function):
    api = get_client()

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
            except TwitterError.TwitterRequestError as e:
                if e.status_code < 420:
                    raise
                elif e.status_code in (420, 429):
                    print(f"Being rate-limited (Status code: {e.status_code})... backing off...")
                    time.sleep(5)
                else:
                    # re-try
                    continue
            except TwitterError.TwitterConnectionError:
                # temporary interruption, re-try request
                continue

    response_iter = _fault_tolerant_response_iter()
    return filter(filter_function,response_iter)
