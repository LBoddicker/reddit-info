import json
import os
import re
import string
import sys
import unicodedata

'''
This module is responsible for parsing comments
'''

def removeUrl(inStr):
    retStr = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', inStr)
    return retStr

def splitToList(inStr):
    words = inStr.split()
    return words

def emojiReplace(inStr):
    retStr = re.sub('[\U0001F600-\U0001F64F]', lambda m: unicodedata.name(m.group()), inStr)
    return retStr

#find out how the translate function works
def removePunc(inStr):
    table = str.maketrans({key: None for key in string.punctuation})
    return inStr.translate(table)

def toLowerCase(inStr):
    return inStr.lower()

def bannedWordFilter(inStr):
    if(inStr == '[removed]' or inStr == '[deleted]'):
        return ''
    else:
        return inStr

def totParse(inStr):
    tempStr = emojiReplace(inStr)
    tempStr = bannedWordFilter(tempStr)
    tempStr = removeUrl(tempStr)
    tempStr = removePunc(tempStr)
    tempStr = toLowerCase(tempStr)
    if (len(tempStr) == 0):
        return '' #empty string
    else:
        return tempStr