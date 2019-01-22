import os
import json
#import sys


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

if __name__ == '__main__':
    tempDict = setupConfig()