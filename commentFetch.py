import sys
import time
import praw
import json
import os
import requests

class InfoFetch():
    """
    This will return a list of comments from a subreddit, user, or submission
    """

    def __init__(self, redditDict):
        self.reddit = praw.Reddit(client_id=redditDict['client_id'],
                                   client_secret=redditDict['client_secret'],
                                   password=redditDict['password'],
                                   user_agent=redditDict['user_agent'],
                                   username=redditDict['username'])

    def getSubmission(self, inSubmission, inLimit=100):
        
        retList = []
        commentDict = {}

        subreddit = self.reddit.subreddit(inSubmission)
        subList = [submission.id for submission in subreddit.top(limit=inLimit)] #make a list of all the subreddit ids
        
        print(subList)

        for i in subList:
            tempStr = 'https://api.pushshift.io/reddit/submission/comment_ids/' + i
            r = requests.get(tempStr)
            j = r.json() 
            commentIds = j["data"]
            commentDict[i] = commentIds #make a dict with submission as key, and comment ids list as value
            print('retrived', i)
            time.sleep(.3)

        trueDict = {}
        for key, val in commentDict.items():
            if len(val) > 1000:
                tempList = []
                loops = len(val) // 1000
                for i in range(loops):
                    tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(val[1000*i:1000*(i+1)])
                    r = requests.get(tempStr)
                    j = r.json()
                    tempList += [i['body'] for i in j['data']]
                    time.sleep(.3)
                tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(val[1000*(i+1):len(val)])
                r = requests.get(tempStr)
                j = r.json()
                tempList += [i['body'] for i in j['data']]
                trueDict[key] = tempList
                time.sleep(.3)
            else:
                tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(val)
                r = requests.get(tempStr)
                j = r.json()
                trueDict[key] = [i['body'] for i in j['data']] #make a dictionary with submisison as id, and comment list as value
                time.sleep(.3)
            print('got comments', key)

        with open('{0}.json'.format(inSubmission), 'w') as newFile:
            json.dump(trueDict, newFile, indent=4, separators=(',', ': '), ensure_ascii=False)

        return retList


if __name__ == '__main__':
    print('infoFetch main running...')

    fetch = InfoFetch()
    #fetch.getSubmission(sys.argv[1])