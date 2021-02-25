# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:31:45 2021

@author: odyss
"""

import os

# from dotenv import load_dotenv
from mongoengine import connect, Document, StringField, DateTimeField


def connect_to_mongo():
    load_dotenv()
    connect(
        os.getenv("web-science"),
        username=os.getenv("web-science"),
        password=os.getenv("web-science"),
        authentication_source='admin'
    )

class Tweet(Document):
    id_str = StringField(unique=True)
    emotion_label = StringField()
    text = StringField(unique=True)
    created_at = DateTimeField()
    meta = {'allow_inheritance': True}


class ProcessedTweet(Document):
    id_str = StringField(unique=True)
    created_at = DateTimeField()
    emotion_label = StringField()
    processed_text = StringField()
    raw_text = StringField()


if __name__ == "__main__":
    connect_to_mongo()
