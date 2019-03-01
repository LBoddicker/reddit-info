# We should return whether or not the comment is positive or negative
# We should return reading level
# We should maintain rankings of most/least positive comments - same with reading level

from textblob import TextBlob
import json

def returnSentiment(inStr):
    myTxt = TextBlob(inStr)
    return myTxt.sentiment.polarity

def getTotSentiment(inSub):
    totNum = 0
    totSentiment = 0
    with open('{0}Parsed.json'.format(inSub)) as readFile:
        d = json.load(readFile)
        for k, v in d.items():
            for i in v:
                totNum += 1
                totSentiment += returnSentiment(i)
                #print(i, returnSentiment(i))
    return totSentiment/totNum
