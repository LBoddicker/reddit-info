import sqlite3
import os

#TODO:
#Add subreddit - name, reddit_id, posts_number, sentiment, comment_number
    #update: posts_number, sentiment, comment_number
#Add submission -  name, reddit_id, subreddit_id, sentiment, comment_number
    #update: sentiment, comment_number
#Add comments -  reddit_id, subreddit_id, submission_id, body, parsed_body, sentiment
    #update: parsed_body, sentiment

#fetch - get a comment, get all comments from a subreddit/submisison


class RedditSQL:
    '''
    This class maintains a databse, providing methods to read and write data.
    '''
    def __init__(self, dbName):
        self.connection = sqlite3.connect("{0}.db".format(dbName)) #open connection if it exists or not
        self.crsr = self.connection.cursor()
        self.dbName = dbName
        self.setup() #check to make sure all the tables are there

    def doesTableExist(self, tableName):
        sql_command = '''SELECT COUNT(*)
                         FROM sqlite_master
                         WHERE type = 'table'
                         AND name = '{0}'
                         '''.format(tableName)
        self.crsr.execute(sql_command)
        if(self.crsr.fetchone()[0] == 1):
            print('the {0} table does exist'.format(tableName))
            return True
        print('the {0} table does NOT exist'.format(tableName))
        return False

    def setup(self):
        if(not self.doesTableExist('subreddits')):
            sql_command = '''CREATE TABLE subreddits 
                            (id INTEGER PRIMARY KEY,
                            name TEXT,
                            reddit_id TEXT,
                            posts_number INTEGER,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('submissions')):
            sql_command = '''CREATE TABLE submissions 
                            (id INTEGER PRIMARY KEY,
                            reddit_id TEXT,
                            subreddit_id INTEGER,
                            name TEXT,
                            comment_number INTEGER,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('comments')):
            sql_command = '''CREATE TABLE comments 
                            (id INTEGER PRIMARY KEY,
                            reddit_id TEXT,
                            subreddit_id INTEGER,
                            submission_id INTEGER,
                            body TEXT,
                            parsed_body TEXT,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        self.connection.commit()
            
    def addSubreddit(self):
        pass

    def addSubmission(self):
        pass

    def addComment(self):
        pass

    def closeDB(self):
        self.connection.close()

if __name__ == '__main__':
    print('RedditSQL.py has been called as main')
    myObj = RedditSQL('test')
    myObj.doesTableExist('subreddits')
    myObj.closeDB()

