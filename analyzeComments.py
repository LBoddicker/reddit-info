# We should return whether or not the comment is positive or negative
# We should return reading level
# We should maintain rankings of most/least positive comments - same with reading level

from textblob import TextBlob
import textstat
import json

def getSentiment(inText):
    blob = TextBlob(inText)
    return (blob.sentiment.polarity, blob.sentiment.subjectivity)

def getReadingScore(inText):
    return textstat.text_standard(inText, float_output=True)

if __name__ == '__main__':
    print(getReadingScore('This test is of the most complicated matter'))