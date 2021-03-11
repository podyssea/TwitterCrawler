from __future__ import print_function
import codecs
import json
import re
import sys

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:42:56 2021

@author: odyss
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Adapted from https://raw.githubusercontent.com/charman/mturk-emoji/master/encode_emoji.py
"""

def replace_emoji_characters(s):
    def _emoji_match_to_span(emoji_match):
        bytes = codecs.encode(emoji_match.group(), 'utf-8')
        bytes_as_json = json.dumps([b for b in bytearray(bytes)])
        return u"<span class='emoji-bytes' data-emoji-bytes='%s'></span>" % \
            bytes_as_json

    # Stripping tweets
    if sys.maxunicode == 1114111:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    elif sys.maxunicode == 65535:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    else:
        raise UnicodeError(
            "Unable to determine if Python was built using UCS-2 or UCS-4")

    return highpoints.sub(_emoji_match_to_span, s)


def main():
    emoji = codecs.open('emoji.txt', encoding='utf-8').read().strip()
    print(replace_emoji_characters(emoji))


if __name__ == "__main__":
    main()
