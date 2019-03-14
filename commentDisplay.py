import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def plotSubredditsReadingScore(inSubreddits, inReadingScores):
    '''
    inSubreddits - tuple of subreddits
    inReadingScores - list of reading scores
    '''
    y_pos = np.arange(len(inSubreddits))

    plt.barh(y_pos, inReadingScores, align='center', alpha=0.5)
    plt.yticks(y_pos, inSubreddits)
    plt.xlabel('Reading Level')
    plt.title('Reading Level of Subreddits')

    plt.show()
