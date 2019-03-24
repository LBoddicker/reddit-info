import os
import json
import commentFetch
import RedditSQL
import praw
import commentParse
import analyzeComments
import commentDisplay
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

def initialSubredditsSetup(commentFetcher, sqlDB, subredditList, submissionLimit = 100):
    for subredditName in subredditList:
        initialSubredditSetup(commentFetcher, sqlDB, subredditName, submissionLimit)

def initialSubredditSetup(commentFetcher, sqlDB, subredditName, submissionLimit = 100):
    '''
    this function assumes that we are starting with a fresh database. That no other data exists.
    Thus we don't have to check if a comment is already there.

    We also make use of the fact that our comments grouped by their submission in the tempList
    '''
    #add subreddit
    tempList = commentFetcher.getCommentsFromSubreddit(subredditName, submissionLimit)
    subredditSQLID = sqlDB.createSubreddit(subredditName)

    lastSubmissionRedditID = ''
    lastSubmissionSQLID = -1
    count = 0

    for commentTuple in tempList:
        count += 1
        if (count % 1000 == 0):
            print('setup - moved through 1000 comments')

        if(commentTuple[1] != lastSubmissionRedditID):
            lastSubmissionRedditID = commentTuple[1]
            lastSubmissionSQLID = sqlDB.createSubmission(subredditSQLID, commentTuple[1])

        sqlDB.createComment(subredditSQLID, lastSubmissionSQLID, commentTuple[2], commentTuple[3])




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
                print('getAndStore - moved through 1000 comments')
            if(not sqlDB.doesCommentExist(commentTuple[2])):                                                 #
                if(not sqlDB.doesSubmissionExist(commentTuple[1])):                                          #
                    submissionSQLID = sqlDB.createSubmission(subredditSQLID, commentTuple[1])                #  
                else:
                    submissionSQLID = sqlDB.getSubmissionSQLID(commentTuple[1])                              #
                sqlDB.createComment(subredditSQLID, submissionSQLID, commentTuple[2], commentTuple[3])       #

def initialParseAllComments(sqlDB):
    
    count = 0
    for i in range(sqlDB.getLengthOfTable('comments')):

        count += 1
        if(count % 1000 == 0):
            print('parse - moved through 1000 comments')

        tempStr = sqlDB.getCommentByID(i+1)[4]
        tempStr = commentParse.totParse(tempStr)
        sqlDB.storeParsedComment(i+1, tempStr)


def initialAnalyze(sqlDB):
    lastSubredditID = sqlDB.getCommentByID(1)[1]
    lastSubmissionID = sqlDB.getCommentByID(1)[2]

    lastReadingCommentCount = 0                #number of comments in a submission
    lastSentimentCommentCount = 0
    lastSubmissionCount = 0             #number of submissions in a subreddit

    runningCommentScore = 0             #sum score of all comments in a submission
    runningCommentPolarity = 0
    runningCommentSubjectivity = 0
    runningSubmissionScore = 0          #sum score of all submissions in a subreddit
    runningSubmissionPolarity = 0
    runningSubmissionSubjectivity = 0

    

    print('we are analyzing comments')
    count = 0

    tableLength = sqlDB.getLengthOfTable('comments')

    for i in range(tableLength):
        count += 1
        if(count % 1000 == 0):
            print('analyze - moved through 1000 comments')

        commentTuple = sqlDB.getCommentByID(i+1)
        #print(commentTuple)

        if(lastSubmissionID != commentTuple[2] or i == tableLength-1):
            newSubmissionScore = (runningCommentScore / lastReadingCommentCount)
            newSubmissionPolarity = (runningCommentPolarity / lastSentimentCommentCount)
            newSubmissionSubjectivity = (runningCommentSubjectivity / lastSentimentCommentCount)

            sqlDB.updateSubmissionReadingScore(lastSubmissionID, newSubmissionScore)
            sqlDB.updateSubmissionPolarity(lastSubmissionID, newSubmissionPolarity)
            sqlDB.updateSubmissionSubjectivity(lastSubmissionID, newSubmissionSubjectivity)

            lastSubmissionCount += 1

            runningSubmissionScore += newSubmissionScore
            runningSubmissionPolarity += newSubmissionPolarity
            runningSubmissionSubjectivity += newSubmissionSubjectivity

            lastReadingCommentCount = 0
            lastSentimentCommentCount = 0
            runningCommentScore = 0
            runningCommentPolarity = 0
            runningCommentSubjectivity = 0
        
        #if this gets triggered then the above must have also been triggered
        if(lastSubredditID != commentTuple[1] or i == tableLength-1): 
            newSubredditScore = runningSubmissionScore / lastSubmissionCount
            newSubredditPolarity = (runningSubmissionPolarity / lastSubmissionCount)
            newSubredditSubjectivity = (runningSubmissionSubjectivity / lastSubmissionCount)

            sqlDB.updateSubredditReadingScore(lastSubredditID, newSubredditScore)
            sqlDB.updateSubredditPolarity(lastSubredditID, newSubredditPolarity)
            sqlDB.updateSubredditSubjectivity(lastSubredditID, newSubredditSubjectivity)

            runningSubmissionScore = 0
            runningSubmissionPolarity = 0
            runningSubmissionSubjectivity = 0
            lastSubmissionCount = 0

        newCommentScore = analyzeComments.getReadingScore(commentTuple[4])
        newCommentPolarity, newCommentSubjectivity = analyzeComments.getSentiment(commentTuple[4])

        sqlDB.updateCommentReadingScore(i+1, newCommentScore)
        sqlDB.updateCommentSubjectivity(i+1, newCommentSubjectivity)
        sqlDB.updateCommentPolarity(i+1, newCommentPolarity)

        if(not commentParse.isBannedWord(commentTuple[4])):
            if(newCommentScore <= 20):
                runningCommentScore += newCommentScore
                lastReadingCommentCount += 1

            runningCommentPolarity += newCommentPolarity
            runningCommentSubjectivity += newCommentSubjectivity
            lastSentimentCommentCount += 1

        lastSubredditID = commentTuple[1]
        lastSubmissionID = commentTuple[2]


def displayData(sqlDB):
    #need to create a tuple of subreddit names
    #need to create a list of reading scores

    tableLength = sqlDB.getLengthOfTable('subreddits')

    subredditNameList = []
    readingScoreList = []
    polarityList = []
    subjectivityList = []

    for i in range(tableLength):
        subredditTuple = sqlDB.getSubredditByID(i+1)
        subredditNameList.append(subredditTuple[1])
        readingScoreList.append(subredditTuple[4])
        polarityList.append(subredditTuple[2])
        subjectivityList.append(subredditTuple[3])

    commentDisplay.plotSubredditReadingScore(subredditNameList, readingScoreList)
    commentDisplay.plotSubredditPolarity(subredditNameList, polarityList)
    commentDisplay.plotSubredditSubjectivity(subredditNameList, subjectivityList)



def main():
    tempDict = setupConfig() #get login info

    #create reddit connection
    redditInstance = praw.Reddit(client_id=tempDict['client_id'],
                                   client_secret=tempDict['client_secret'],
                                   password=tempDict['password'],
                                   user_agent=tempDict['user_agent'],
                                   username=tempDict['username'])

    sqlDB = RedditSQL.RedditSQL(DB_NAME) #create SQL interface object

    myInst = commentFetch.InfoFetch(redditInstance, sqlDB) #create comment grabber object

    listOfSubs = ['announcements', 'funny', 'AskReddit', 'todayilearned', 'science', 'worldnews', 'pics', 'IAmA', 'gaming', 'videos',
                  'movies', 'aww', 'Music', 'blog','gifs','news','explainlikeimfive','askscience','EarthPorn','books',
                  'television','mildlyinteresting','LifeProTips','Showerthoughts','space','DIY','Jokes','gadgets','nottheonion','sports',
                  'tifu','food','photoshopbattles','Documentaries','Futurology','history','InternetIsBeautiful','dataisbeautiful','UpliftingNews','listentothis',
                  'GetMotivated','personalfinance','OldSchoolCool','philosophy','Art','nosleep','WritingPrompts','creepy','TwoXChromosomes','Fitness',
                  'technology','WTF','bestof','AdviceAnimals','politics','atheism','interestingasfuck','europe','woahdude','BlackPeopleTwitter',
                  'oddlysatisfying','gonewild','leagueoflegends','pcmasterrace','reactiongifs','gameofthrones','wholesomememes','Unexpected','Overwatch','facepalm',
                  'trees','Android','lifehacks','me_irl','relationships','Games','nba','programming','tattoos','NatureIsFuckingLit',
                  'Whatcouldgowrong','CrappyDesign','Dankmemes','nsfw','cringepics','4chan','soccer','comics','sex','pokemon',
                  'malefashionadvice','NSFW_GIF','StarWars','Frugal','HistoryPorn','AnimalsBeingJerks','RealGirls','travel','buildapc','OutOfTheLoop']

    testListOfSubs = ['announcements', 'funny', 'AskReddit', 'todayilearned', 'science', 'worldnews', 'pics', 'IAmA', 'gaming', 'videos',
                  'movies', 'aww', 'Music', 'blog','gifs','news','explainlikeimfive','askscience','EarthPorn','books']
    
    
    initialSubredditsSetup(myInst, sqlDB, listOfSubs, 5)

    initialParseAllComments(sqlDB)

    initialAnalyze(sqlDB)

    sqlDB.getSubredditTable()

    sqlDB.getSubmissionTable()

    displayData(sqlDB)

    sqlDB.closeDB()

    

if __name__ == '__main__':
    print(sys.argv)
    main()