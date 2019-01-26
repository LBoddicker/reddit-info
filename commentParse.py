import json
import os
import re
import string
import sys
import unicodedata

#the purpose of this class is to take in a group of comments from a subreddit
#and then return parsed comments though the iterator

class ParseComments():

    def __init__(self, inSubreddit, removeList = None):
        if(not os.path.exists('{0}.json'.format(inSubreddit))):
            raise Exception('File does not exist!')
        else:
            self.mySub = inSubreddit #string name of python library
            self.removeList = removeList
            self.parse(inSubreddit)
            

    def __iter__(self):
        if(not os.path.exists('{0}Parsed.json'.format(self.mySub))):
            raise Exception('File does not exist!')
        else:
            with open('{0}Parsed.json'.format(self.mySub)) as readFile:
                d = json.load(readFile)
                for k, v in d.items():
                    for i in v:
                        yield i

    def parse(self, subredditName):
        parsedDict = {}
        with open('{0}.json'.format(self.mySub)) as readFile:
            d = json.load(readFile)
            for k, v in d.items():
                tempList = []
                for i in v:
                    tempCom = totParse(i)
                    if(tempCom is not None):
                        tempList.append(totParse(i))
                parsedDict[k] = tempList 

        with open('{0}Parsed.json'.format(self.mySub), 'w') as newFile:
            json.dump(parsedDict, newFile, indent=4, separators=(',', ': '), ensure_ascii=False)

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
        return None
    else:
        return tempStr
    
def main(inSubmission):
    myObj = ParseComments(inSubmission)

    for x in myObj:
        print(x)

if __name__ == '__main__':
    main(sys.argv[1])