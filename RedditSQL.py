import sqlite3

class RedditSQL:
    '''
    The purpose of this class is to provide 
    '''
    def __init__(self, dbName):
        self.connection = sqlite3.connect("{0}.db".format(dbName))
        self.crsr = self.connection.cursor()

    def setup(self):
        sql_command = '''CREATE TABLE subreddits 
                         (id INTEGER PRIMARY KEY,
                         name TEXT,
                         reddit_id TEXT,
                         posts_number INTEGER,
                         sentiment TEXT);
                          '''
        self.crsr.execute(sql_command)
        sql_command = '''CREATE TABLE submissions 
                         (id INTEGER PRIMARY KEY,
                         reddit_id TEXT,
                         subreddit_id INTEGER,
                         name TEXT,
                         comment_number INTEGER,
                         sentiment TEXT);
                          '''
        self.crsr.execute(sql_command)
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
        sql_command = '''INSERT INTO subreddits (name, reddit_id, posts_number, sentiment) VALUES
                         ('testSub', 'aaaa', 42, '1.00');
                          '''
        self.crsr.execute(sql_command)
        self.connection.commit()

    def addSubreddit(self):
        pass

    def addComments(self):
        pass

    def addSubmission(self):
        pass

    def getInfo(self):
        sql_command = '''SELECT name FROM sqlite_master 
                         WHERE type='table' 
                         AND name='subreddits'
                         '''
        self.crsr.execute(sql_command)
        ans = self.crsr.fetchall()
        for i in ans:
            print(i)

        self.crsr.execute("SELECT * FROM subreddits;")
        ans = self.crsr.fetchall()
        for i in ans:
            print(i)
        print('getInfo has finished')

    def closeDB(self):
        self.connection.close()

    

if __name__ == '__main__':
    print('main has been called')
    myObj = RedditSQL('test')
    myObj.setup()
    myObj.getInfo()
    myObj.closeDB()

