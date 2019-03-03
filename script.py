import os
import json
import commentFetch
import RedditSQL
import praw
#from commentParse import ParseComments
#from analyzeComments import *
import sys

# New rules/ideas
## the will deal with the pulling from SQL and storing to SQL here -- the other modules/classes will not be responsible for that

DB_NAME = 'reddit_database'

def setupConfig():
    myConfigDict = {}

    if(os.path.exists('redditConfig.json')):
        print('it does exist')
        with open('redditConfig.json') as of:
            myConfigDict = json.load(of)

    else:
        keys = ['user_agent', 'client_id', 
                'client_secret', 'username',
                'password']

        print('Config file does not exist. Lets make one')

        for k in keys:
            myConfigDict[k] = input('!!! '+k+' :')

        with open('redditConfig.json', 'w') as fp:
            json.dump(myConfigDict, fp)

    return myConfigDict


def getAndStoreSubreddits(commentFetcher, sqlDB, subredditList, submissionLimit = 100):
    '''
    commentFetcher - object of class InfoFetch
    sqlDB - object of class RedditSQL
    subredditList - list of strings
    submisisonLimit - int

    This class will grab all comments from the top 'submissionLimit' number of posts
    from each subreddit and store them in the SQL database.

    Notes: If a subreddit is already stored in the sql database it will not check to see
    if the comments are also there. It will assume the comments are there.
    '''
    for subredditName in subredditList:
        getAndStoreSubreddit(commentFetcher, sqlDB, subredditName, submissionLimit)


def getAndStoreSubreddit(commentFetcher, sqlDB, subredditName, submissionLimit = 100):
    '''
    commentFetcher - object of class InfoFetch
    sqlDB - object of class RedditSQL
    subredditName - string
    submisisonLimit - int

    This class will grab all comments from the top 'submissionLimit' number of posts
    and store them in the SQL database.

    Notes: If a subreddit is already stored in the sql database it will not check to see
    if the comments are also there. It will assume the comments are there.
    '''
    print('Started subreddit: ', subredditName)
    if(not sqlDB.doesSubredditExist(subredditName)):
        tempList = commentFetcher.getCommentsFromSubreddit(subredditName, submissionLimit)
        subredditSQLID = sqlDB.createSubreddit(subredditName)

        count = 0
        for commentTuple in tempList:
            count += 1
            if (count % 1000 == 0):
                print('moved thourhg 1000 comments')
            if(not sqlDB.doesCommentExist(commentTuple[2])):
                if(not sqlDB.doesSubmissionExist(commentTuple[1])):
                    submissionSQLID = sqlDB.createSubmission(subredditSQLID, commentTuple[1])  
                else:
                    submissionSQLID = sqlDB.getSubmissionSQLID(commentTuple[1])
                sqlDB.createComment(subredditSQLID, submissionSQLID, commentTuple[2], commentTuple[3])


    

def main():
    tempDict = setupConfig() #get login info

    #create reddit connection
    redditInstance = praw.Reddit(client_id=tempDict['client_id'],
                                   client_secret=tempDict['client_secret'],
                                   password=tempDict['password'],
                                   user_agent=tempDict['user_agent'],
                                   username=tempDict['username'])

    sqlConnection = RedditSQL.RedditSQL(DB_NAME) #create SQL interface object

    myInst = commentFetch.InfoFetch(redditInstance, sqlConnection) #create comment grabber object

    listOfSubs = ['announcements', 'funny', 'AskReddit', 'todayilearned', 'science', 'worldnews', 'pics', 'IAmA', 'gaming', 'videos',
                  'movies', 'aww', 'Music', 'blog','gifs','news','explainlikeimfive','askscience','EarthPorn','books',
                  'television','mildlyinteresting','LifeProTips','Showerthoughts','space','DIY','Jokes','gadgets','nottheonion','sports',
                  'tifu','food','photoshopbattles','Documentaries','Futurology','history','InternetIsBeautiful','dataisbeautiful','UpliftingNews','listentothis',
                  'GetMotivated','personalfinance','OldSchoolCool','philosophy','Art','nosleep','WritingPrompts','creepy','TwoXChromosomes','Fitness',
                  'technology','WTF','bestof','AdviceAnimals','politics','athesim','interestingasfuck','europe','woahdude','BlackPeopleTwitter',
                  'oddlysatisfying','gonewild','leagueoflegends','pcmasterrace','reactiongifs','gameofthrones','wholesomememes','Unexpected','Overwatch','facepalm',
                  'trees','Android','lifehacks','me_irl','relationships','Games','nba','programming','tattoos','NatureIsFuckingLit',
                  'Whatcouldgowrong','CrappyDesign','Dankmemes','nsfw','cringepics','4chan','soccer','comics','sex','pokemon',
                  'malefashionadvice','NSFW_GIF','StarWars','Frugal','HistoryPorn','AnimalsBeingJerks','RealGirls','travel','buildapc','OutOfTheLoop']
    
    
    getAndStoreSubreddits(myInst, sqlConnection, listOfSubs, 5)

    sqlConnection.getSubredditTable()

if __name__ == '__main__':
    print(sys.argv)
    main()