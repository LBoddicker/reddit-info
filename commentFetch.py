import sys
import time
import praw
import json
import os
import requests
import RedditSQL

## CURRENT QUESTIONS
# We need 

class InfoFetch():
    """
    This will return a list of comments from a subreddit, user, or submission
    """

    def __init__(self, redditInstance, sqlConnection):
        self.redditInstance = redditInstance
        self.sqlConnection = sqlConnection

    def getCommentsFromSubreddit(self, inSubreddit, submissionLimit = 100):
        # Check to see if we already have the subreddit
        ## If we do not we make a subreddit entry in the database
        ## We gather a list of submissions
        ## We call getSubmissionComments()

        if(not self.sqlConnection.existsInSubredditTable(inSubreddit)):
            

            try:
                self.sqlConnection.addSubreddit(inSubreddit) 
                subreddit = self.redditInstance.subreddit(inSubreddit)
                subList = [submission.id for submission in subreddit.top(limit=submissionLimit)]
                for i in subList:
                    self.getSubmissionComments(i, 1)
            except:
                print('Something went wrong in getCommentsFromSubreddit()')

    def getSubmissionComments(self, inSubmission, subredditID):
        #We get all the comment ideas
        #We check to see if they already exist
        ## If they do not already exist we add them
        pass



    def getSubmission(self, inSubmission, inLimit=100):
        '''
        This method takes a subreddit and returns all of that subreddit's comments
        '''
        if(not os.path.exists('{0}.json'.format(inSubmission))):
            retList = []
            commentDict = {}

            subreddit = self.reddit.subreddit(inSubmission)
            subList = [submission.id for submission in subreddit.top(limit=inLimit)] #make a list of all the submission ids
            
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


if __name__ == '__main__':
    print('infoFetch main running...')

    fetch = InfoFetch()
    #fetch.getSubmission(sys.argv[1])