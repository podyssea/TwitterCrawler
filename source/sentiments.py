# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:23:20 2021

@author: odyss
"""

import string


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
        
        #filter out the emoji from the term
        def _filter_emoji(match_term):
            return len(match_term) > 1 or match_term.lower() in string.ascii_lowercase
        
        #remove the hashtag from the term, replace it with empty
        def _remove_hashtags(match_term):
            return match_term.replace("#", "")
        
        emotion_words_dict[emotion] = list(map(_remove_hashtags, filter(_filter_emoji, match_terms)))

    return emotion_words_dict