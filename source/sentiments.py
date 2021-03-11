# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:23:20 2021

@author: odyss
"""

import string

#define the emotion map classes
EMOTION_CLASS_MAP = {
    "excitement": ["#excited", "#excitement", "😁"],
    "happy": ["#happy", "#joy", "#love", "😀", ":)"],
    "pleasant": ["#pleasant", "#calm", "#positive", "🙂"],
    "surprise": ["#sad", "#frustrated", "#negative", "😧", "😮", ":("],
    "fear": ["#scared", "#afraid", "#disgusted", "#depressed", "😳", "😢", "😨"],
    "anger": ["#angry", "#mad", "#raging", "😡", "😠", "☹️"]
}


def get_emotion_words_dict():

    emotion_words_dict = {}

    for emotion, match_terms in EMOTION_CLASS_MAP.items():

        #filter out the emoji from the text
        def _remove_emoji(match_term):
            return len(match_term) > 1 or match_term.lower() in string.ascii_lowercase

        #remove the hashtags from the text, replace it with empty string
        def _remove_hashtags(match_term):
            return match_term.replace("#", "")

        emotion_words_dict[emotion] = list(map(_remove_hashtags, filter(_remove_emoji, match_terms)))

    return emotion_words_dict
