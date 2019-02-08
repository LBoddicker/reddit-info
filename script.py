import os
import json
import commentFetch
import RedditSQL
import praw
from commentParse import ParseComments
from analyzeComments import *
import sys


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

def main():
    tempDict = setupConfig()
    redditInstance = praw.Reddit(client_id=tempDict['client_id'],
                                   client_secret=tempDict['client_secret'],
                                   password=tempDict['password'],
                                   user_agent=tempDict['user_agent'],
                                   username=tempDict['username'])
    sqlConnection = RedditSQL.RedditSQL('myDB')
    myInst = commentFetch.InfoFetch(redditInstance, sqlConnection)
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
    tempList = []
    for i in listOfSubs:
        myInst.getCommentsFromSubreddit(i, submissionLimit=100)
    sqlConnection.getSubredditTable()


if __name__ == '__main__':
    print(sys.argv)
    main()