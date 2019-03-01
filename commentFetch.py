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

        return a dictionary with the subreddit as key and a dictionary with the submission/comment data as value
        '''
        for i in inSubredditList:
            self.getCommentsFromSubreddit(i, submissionLimit)


    def getCommentsFromSubreddit(self, inSubreddit, submissionLimit = 100):
        '''
        inSubreddit - string
        submissionLimit - int

        return a dictionary with the submission_id as key and value as a list of tupes (comment_body, comment_id)

        will fetch from a subreddit all the comments of the top posts.
        '''

        if(not self.sqlConnection.existsInSubredditTable(inSubreddit)):
            try:
                self.sqlConnection.addSubreddit(inSubreddit) 
                subreddit = self.redditInstance.subreddit(inSubreddit)
                subList = [submission.id for submission in subreddit.top(limit=submissionLimit)]
                for i in subList:
                    self.getSubmissionComments(inSubreddit, i)
            except:
                print('Something went wrong in getCommentsFromSubreddit()')
    

    def getSubmissionComments(self, submissionID):
        '''
        subredditName - string
        submisisonID - string

        return a list of tuples (comment_body, comment_id)

        will fetch and store all the comments from a specified post.
        '''

        tempStr = 'https://api.pushshift.io/reddit/submission/comment_ids/' + submissionID
        r = requests.get(tempStr)
        j = r.json() 
        commentIds = j["data"]
        time.sleep(.3)

        if len(commentIds) > 1000:
            tempList = []
            loops = len(commentIds) // 1000
            for i in range(loops):
                tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds[1000*i:1000*(i+1)])
                r = requests.get(tempStr)
                j = r.json()
                zipList = list(zip( [i['body'] for i in j['data']], commentIds[1000*i:1000*(i+1)] ))
                tempList += zipList
                time.sleep(.3)
            tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds[1000*(i+1):len(commentIds)])
            r = requests.get(tempStr)
            j = r.json()
            zipList = list(zip( [i['body'] for i in j['data']], commentIds[1000*(i+1):len(commentIds)] ))
            tempList += zipList
            time.sleep(.3)
        else:
            tempStr = 'https://api.pushshift.io/reddit/comment/search?ids=' + ','.join(commentIds)
            r = requests.get(tempStr)
            j = r.json()
            zipList = list(zip([i['body'] for i in j['data']], commentIds))
            tempList += zipList
            time.sleep(.3)

        return tempList

        
        

if __name__ == '__main__':
    print('main was called')