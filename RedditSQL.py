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
                            sentiment_polarity REAL,
                            sentiment_subjectivity REAL,
                            reading_score REAL);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('submissions')):
            sql_command = '''CREATE TABLE submissions 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            subreddit_sql_id INTEGER,
                            submission_reddit_id TEXT,
                            sentiment_polarity REAL,
                            sentiment_subjectivity REAL,
                            reading_score REAL);
                            '''
            self.crsr.execute(sql_command)

        if(not self.doesTableExist('comments')):
            sql_command = '''CREATE TABLE comments 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            subreddit_sql_id INTEGER,
                            submission_sql_id INTEGER,
                            comment_reddit_id TEXT,
                            body TEXT,
                            parsed_body TEXT,
                            sentiment_polarity REAL,
                            sentiment_subjectivity REAL,
                            reading_score REAL);
                            '''
            self.crsr.execute(sql_command)

        self.connection.commit()

    def getSubredditTable(self):
        sql_command = '''SELECT * 
                         FROM subreddits'''
        self.crsr.execute(sql_command)
        for row in self.crsr:
            print(row)

    def getSubmissionTable(self):
        sql_command = '''SELECT * 
                         FROM submissions'''
        self.crsr.execute(sql_command)
        for row in self.crsr:
            print(row)

    def getCommentTable(self):
        sql_command = '''SELECT * 
                         FROM comments'''
        self.crsr.execute(sql_command)
        for row in self.crsr:
            print(row)


    

    def addSubreddit(self, subredditName):
        if(not self.doesSubredditExist(subredditName)):
            sql_command = '''INSERT INTO subreddits
                            (name)
                            VALUES ("{0}");
                            '''.format(subredditName)
            self.crsr.execute(sql_command)
            self.connection.commit()

    def addCommentsFromSubmission(self, subredditName, submissionID, commentID, commentBody):
        '''
        subreddit - string
        submissionID - string
        commentID - list of strings
        commentBody - list of strings
        Takes many commentIDs and commentBodys from a submisison and adds them to SQL database

        commentID and commentBody must be the same length
        '''
        if(len(commentID) != len(commentBody)):
            raise Exception('FUNC: addCommentsFromSubmission -- commentID and commentBody not the same length!')

        for i in range(len(commentID)):
            self.addComment(subredditName, submissionID, commentID[i], commentBody[i])


    def addComment(self, subredditName, submissionID, commentID, commentBody):
        '''
        subreddit - string
        submissionID - string
        commentID - string
        commentBody - string
        store a single comment in the SQL database
        '''
        sql_command = '''INSERT INTO comments
                         (subredditName, submission_id, comment_id, body)
                         VALUES ("{0}", "{1}", "{2}", "{3}")
                         '''.format(subredditName, submissionID, commentID, commentBody)
        self.crsr.execute(sql_command)
        self.connection.commit()


    def doesSubredditExist(self, subredditName):
        '''
        subredditName - string
        output - True/False

        returns true if subreddit exists in SQL database
        '''
        sql_command = '''SELECT COUNT(*) 
                        FROM subreddits
                        WHERE name = "{0}"
                        '''.format(subredditName)
        self.crsr.execute(sql_command)
        data = self.crsr.fetchone()[0]
        if(data == 0):
            return False
        else:
            return True

    def createSubreddit(self, subredditName):
        '''
        subredditName - string
        output - SQL ID

        will create a subreddit and return its SQL ID
        '''
        sql_command = '''INSERT INTO subreddits
                         (name)
                         VALUES ("{0}")
                         '''.format(subredditName)
        self.crsr.execute(sql_command)
        self.connection.commit()

        return self.crsr.lastrowid

    def getSubredditSQLID(self, subredditName):
        '''
        subredditName - string
        output - SQL ID

        will return the SQL ID
        '''
        sql_command = '''
                      SELECT id
                      FROM subreddits
                      WHERE name = "{0}"
                      '''.format(subredditName)
        self.crsr.execute(sql_command)
        return self.crsr.fetchone()[0]

    def getSubredditByID(self, subredditID):
        '''
        subredditID - the SQL subreddit ID - int
        output - tuple of the subreddit
        '''
        #TODO: fix parsed body spelling

        sql_command = '''SELECT *
                         FROM subreddits
                         WHERE
                         id = ?
                         '''
        self.crsr.execute(sql_command, (subredditID,))
        return self.crsr.fetchone()


    def doesSubmissionExist(self, submissionRedditID):
        '''
        submissionRedditID - string
        output - True/False

        returns true if submission exists in SQL database
        '''
        sql_command = '''SELECT COUNT(*) 
                        FROM submissions
                        WHERE submission_reddit_id = "{0}"
                        '''.format(submissionRedditID)
        self.crsr.execute(sql_command)
        data = self.crsr.fetchone()[0]
        if(data == 0):
            return False
        else:
            return True

    def createSubmission(self, subredditSQLID, submissionRedditID):
        '''
        subredditSQLID - int
        submissionRedditID - string
        output - SQL ID

        will create a submission and return its SQL ID
        '''
        sql_command = '''INSERT INTO submissions
                         (subreddit_sql_id, submission_reddit_id)
                         VALUES ({0}, "{1}")
                         '''.format(subredditSQLID, submissionRedditID)
        self.crsr.execute(sql_command)
        self.connection.commit()

        return self.crsr.lastrowid

    def getSubmissionSQLID(self, submissionRedditID):
        '''
        submissionRedditID - string
        output - SQL ID

        will return the SQL ID
        '''

        sql_command = '''
                      SELECT id
                      FROM submissions
                      WHERE submission_reddit_id = "{0}"
                      '''.format(submissionRedditID)
        self.crsr.execute(sql_command)
        return self.crsr.fetchone()[0]


    def doesCommentExist(self, commentRedditID):
        '''
        commentRedditID - string
        output - True/False

        returns true if submission exists in SQL database
        '''
        sql_command = '''SELECT COUNT(*) 
                        FROM comments
                        WHERE comment_reddit_id = "{0}"
                        '''.format(commentRedditID)
        self.crsr.execute(sql_command)
        data = self.crsr.fetchone()[0]
        if(data == 0):
            return False
        else:
            return True

    def createComment(self, subredditSQLID, submissionSQLID, commentRedditID, commentBody):
        '''
        subredditSQLID - int
        submissionSQLID - int
        commentRedditID - string
        commentBody - string
        output - SQL ID

        will create a submission and return its SQL ID
        '''
        sql_command = '''INSERT INTO comments
                         (subreddit_sql_id, submission_sql_id, comment_reddit_id, body)
                         VALUES (?, ?, ?, ?)
                         '''
        self.crsr.execute(sql_command, (subredditSQLID, submissionSQLID, commentRedditID, commentBody))
        self.connection.commit()

        return self.crsr.lastrowid

    def getCommentSQLID(self, commentRedditID):
        '''
        commentRedditID - string
        output - SQL ID

        will return the SQL ID
        '''
        sql_command = '''
                      SELECT id
                      FROM comments
                      WHERE comment_reddit_id  = "{0}"
                      '''.format(commentRedditID)
        self.crsr.execute(sql_command)
        return self.crsr.fetchone()[0]

    def getLengthOfTable(self, tableName):
        '''
        tableName - string
        output - int
        '''
        #NOTE: tables can not be the target of parameter substitutaion
        #right now this can be injected with something bad :(
        #should fix in the future
        sql_command = '''SELECT COUNT(*)
                         FROM {0}
                         '''.format(tableName)
        self.crsr.execute(sql_command)
        return self.crsr.fetchone()[0]

    def getCommentByID(self, commentID):
        '''
        commentID - the SQL comment ID
        output - tuple of the comment -- (id, subreddit_sql_id, submission_sql_id, comment_reddit_id, body, parsed_body, sentiment)
        '''
        #TODO: fix parsed body spelling

        sql_command = '''SELECT *
                         FROM comments
                         WHERE
                         id = ?
                         '''
        self.crsr.execute(sql_command, (commentID,))
        return self.crsr.fetchone()

    def storeParsedComment(self, commentID, parsedCommentBody):
        sql_command = '''UPDATE comments
                         SET (parsed_body) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (parsedCommentBody, commentID))
        self.connection.commit()

    def updateSubmissionReadingScore(self, submissionID, score):
        '''
        submissionID - int
        score - float
        '''
        sql_command = '''UPDATE submissions
                         SET (reading_score) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, submissionID))
        self.connection.commit()

    def updateSubredditReadingScore(self, subredditID, score):
        '''
        subredditID - int
        score - float
        '''
        sql_command = '''UPDATE subreddits
                         SET (reading_score) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, subredditID))
        self.connection.commit()

    def updateCommentReadingScore(self, commentID, score):
        '''
        commentID - int
        score - float
        '''
        sql_command = '''UPDATE comments
                         SET (reading_score) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, commentID))
        self.connection.commit()

    def updateSubredditPolarity(self, subredditID, score):
        '''
        subredditID - int
        score - float
        '''
        sql_command = '''UPDATE subreddits
                         SET (sentiment_polarity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, subredditID))
        self.connection.commit()
        
    def updateSubredditSubjectivity(self, subredditID, score):
        '''
        subredditID - int
        score - float
        '''
        sql_command = '''UPDATE subreddits
                         SET (sentiment_subjectivity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, subredditID))
        self.connection.commit() 

    def updateSubmissionPolarity(self, submissionID, score):
        '''
        submissionID - int
        score - float
        '''
        sql_command = '''UPDATE submissions
                         SET (sentiment_polarity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, submissionID))
        self.connection.commit()
        
    def updateSubmissionSubjectivity(self, submissionID, score):
        '''
        submissionID - int
        score - float
        '''
        sql_command = '''UPDATE submissions
                         SET (sentiment_subjectivity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, submissionID))
        self.connection.commit() 

    def updateCommentPolarity(self, commentID, score):
        '''
        commentID - int
        score - float
        '''
        sql_command = '''UPDATE comments
                         SET (sentiment_polarity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, commentID))
        self.connection.commit()
        
    def updateCommentSubjectivity(self, commentID, score):
        '''
        commentID - int
        score - float
        '''
        sql_command = '''UPDATE comments
                         SET (sentiment_subjectivity) = ?
                         WHERE id = ?
                         '''
        self.crsr.execute(sql_command, (score, commentID))
        self.connection.commit()

    def displayTopCommentsBySubmission(self, submissionID, num):
        sql_command = '''SELECT *
                         FROM comments
                         WHERE submission_sql_id = ?
                         ORDER BY reading_score DESC
                         LIMIT ?
                         '''
        self.crsr.execute(sql_command, (submissionID, num))
        
        rows = self.crsr.fetchall()
        for row in rows:
            print(row)
        
        return rows

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
    myObj.doesSubredditExist('pics')
    myObj.doesSubredditExist('blah')
    myObj.closeDB()