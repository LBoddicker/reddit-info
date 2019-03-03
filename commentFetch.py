import sys
import time
import praw
import json
import os
import requests
import RedditSQL

class InfoFetch():
    """
    This class is responsible for fetching comments
    """

    def __init__(self, redditInstance, sqlConnection):
        self.redditInstance = redditInstance
        self.sqlConnection = sqlConnection

    def getCommentsFromSubreddits(self, inSubredditList, submissionLimit = 100):
        '''
        inSubredditList - list of strings
        submissionLimit - int
        will fetch comments for all the subreddits in the list

        return a list of tuples (subreddit_name, submission_reddit_id, comment_reddit_id, comment_body)

        Notes: maybe don't use this so much as it may use a lot of memory
        '''
        retList = []
        for i in inSubredditList:
            retList += self.getCommentsFromSubreddit(i, submissionLimit)
            print('we comments from: ', i)

        return retList


    def getCommentsFromSubreddit(self, inSubreddit, submissionLimit = 100):
        '''
        inSubreddit - string
        submissionLimit - int

        return a list of tuples (subreddit_name, submission_reddit_id, comment_reddit_id, comment_body)

        will fetch from a subreddit all the comments of the top posts.
        '''
        print('we are starting to fetch comments from:', inSubreddit)

        if(not self.sqlConnection.doesSubredditExist(inSubreddit)):
            retList = []
            tempList = []

            self.sqlConnection.addSubreddit(inSubreddit) 
            subreddit = self.redditInstance.subreddit(inSubreddit)
            subList = [submission.id for submission in subreddit.top(limit=submissionLimit)]
            for i in subList:
                tempList += self.getSubmissionComments(i)

            for i in tempList:
                retList.append((inSubreddit,) + i)

            return retList
        return []
    

    def getSubmissionComments(self, submissionID):
        '''
        subredditName - string
        submisisonID - string

        return a list of tuples (submission_reddit_id, comment_reddit_id, comment_body)

        will fetch and store all the comments from a specified post.
        '''
        print('starting to fetch comments from submission: ', submissionID)

        tempStr = 'https://api.pushshift.io/reddit/submission/comment_ids/' + submissionID
        r = requests.get(tempStr)
        j = r.json() 
        commentIds = j["data"]
        time.sleep(.3)

        if len(commentIds) > 1000:
            retList = []
            loops = len(commentIds) // 1000
            for i in range(loops):
                tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds[1000*i:1000*(i+1)])
                r = requests.get(tempStr)
                j = r.json()
                zipList = list(zip([submissionID for i in range(1000)], commentIds[1000*i:1000*(i+1)], [i['body'] for i in j['data']]))
                retList += zipList
                time.sleep(.3)
            tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds[1000*(i+1):len(commentIds)])
            r = requests.get(tempStr)
            j = r.json()
            zipList = list(zip([submissionID for i in range(len(commentIds)%1000)], commentIds[1000*(i+1):len(commentIds)], [i['body'] for i in j['data']]))
            retList += zipList
            time.sleep(.3)
        else:
            tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds)
            r = requests.get(tempStr)
            j = r.json()
            zipList = list(zip([submissionID for i in range(len(commentIds))], commentIds, [i['body'] for i in j['data']]))
            retList += zipList
            time.sleep(.3)

        return retList

if __name__ == '__main__':
    print('main was called')