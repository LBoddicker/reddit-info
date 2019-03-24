import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def plotSubredditReadingScore(inSubreddits, inReadingScores):
    '''
    inSubreddits - List of subreddits
    inReadingScores - list of reading scores
    '''
    def takeSecond(elem):
        return elem[1]

    zipped = list(zip(inSubreddits, inReadingScores))
    print(zipped)
    zipped.sort(key=takeSecond)
    print(zipped)

    inSubreddits, inReadingScores = zip(*list(zipped))


    y_pos = np.arange(len(inSubreddits))

    plt.barh(y_pos, inReadingScores, align='center', alpha=0.5)
    plt.yticks(y_pos, inSubreddits)
    plt.xlabel('Reading Level')
    plt.title('Reading Level of Subreddits')

    plt.show()

def plotSubredditPolarity(inSubreddits, inReadingScores):
    '''
    inSubreddits - List of subreddits
    inReadingScores - list of reading scores
    '''
    def takeSecond(elem):
        return elem[1]

    zipped = list(zip(inSubreddits, inReadingScores))
    print(zipped)
    zipped.sort(key=takeSecond)
    print(zipped)

    inSubreddits, inReadingScores = zip(*list(zipped))


    y_pos = np.arange(len(inSubreddits))

    plt.barh(y_pos, inReadingScores, align='center', alpha=0.5)
    plt.yticks(y_pos, inSubreddits)
    plt.xlabel('Polarity')
    plt.title('Polarity of Subreddits')

    plt.show()

def plotSubredditSubjectivity(inSubreddits, inReadingScores):
    '''
    inSubreddits - List of subreddits
    inReadingScores - list of reading scores
    '''
    def takeSecond(elem):
        return elem[1]

    zipped = list(zip(inSubreddits, inReadingScores))
    print(zipped)
    zipped.sort(key=takeSecond)
    print(zipped)

    inSubreddits, inReadingScores = zip(*list(zipped))


    y_pos = np.arange(len(inSubreddits))

    plt.barh(y_pos, inReadingScores, align='center', alpha=0.5)
    plt.yticks(y_pos, inSubreddits)
    plt.xlabel('Subjectivity')
    plt.title('Subjectivity of Subreddits')

    plt.show()