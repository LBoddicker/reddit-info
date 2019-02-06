import sqlite3
import os

class RedditSQL:
    '''
    This class maintains a databse, providing methods to read and write data.
    '''
    def __init__(self, dbName):
        '''
        Creates an instance of and SQL database manager.
        Has a connection and a cursor to the database.
        Checks to see if the tables exist and if they do not it will create them
        '''
        self.connection = sqlite3.connect("{0}.db".format(dbName)) #open connection if it exists or not
        self.crsr = self.connection.cursor()
        self.dbName = dbName
        self.setup() #check to make sure all the tables are there

    def doesTableExist(self, tableName):
        '''
        returns True if the table exists and False if it does not
        '''
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
        '''
        This method will check to see if it has each of the three necessary tables
        '''
        if(not self.doesTableExist('subreddits')):
            sql_command = '''CREATE TABLE subreddits 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('submissions')):
            sql_command = '''CREATE TABLE submissions 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            reddit_id TEXT,
                            subreddit_id INTEGER,
                            name TEXT,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('comments')):
            sql_command = '''CREATE TABLE comments 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            reddit_id TEXT,
                            subreddit_id INTEGER,
                            submission_id INTEGER,
                            body TEXT,
                            parsed_body TEXT,
                            sentiment TEXT);
                            '''
            self.crsr.execute(sql_command)

        self.connection.commit()

    def getSubredditTable(self):
        sql_command = '''SELECT * 
                         FROM subreddits'''
        self.crsr.execute(sql_command)
        for row in self.crsr:
            print(row)
            
    def existsInSubredditTable(self, subredditName):
        sql_command = '''SELECT COUNT(*) 
                         FROM subreddits
                         WHERE name = "{0}"
                         '''.format(subredditName)
        self.crsr.execute(sql_command)
        data = self.crsr.fetchone()[0]
        if(data == 0):
            print('it does not exists')
            return False
        else:
            print('it exists')
            return True

    def addSubreddit(self, subredditName):
        if(not self.existsInSubredditTable(subredditName)):
            sql_command = '''INSERT INTO subreddits
                            (name)
                            VALUES ("{0}");
                            '''.format(subredditName)
            self.crsr.execute(sql_command)
            self.connection.commit()

    def addSubmission(self):
        pass

    def addComment(self):
        pass

    def doesSubredditExist(self):
        pass

    def doesSubmissionExist(self):
        pass

    def closeDB(self):
        '''
        closes connection to the database
        '''
        self.connection.close()

if __name__ == '__main__':
    print('RedditSQL.py has been called as main')
    myObj = RedditSQL('test')
    myObj.addSubreddit('testTwo')
    myObj.addSubreddit('programming')
    myObj.addSubreddit('pics')
    myObj.getSubredditTable()
    myObj.existsInSubredditTable('pics')
    myObj.existsInSubredditTable('blah')
    myObj.closeDB()

