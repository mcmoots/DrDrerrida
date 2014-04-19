# This script pulls random lyrics/quotes from two files
# and mashes them together to make one <140 character tweet

QUOTEF1 = 'dre_quotes.txt'
QUOTEF2 = 'derrida_quotes.txt'

TWEETSIZE = 140
MAXTRIES = 500

import random
import twitter
import yaml

# load api keys from config file
twitter_tokens = yaml.load(open('config.yaml'))
api = twitter.Api(**twitter_tokens)

def parsequotes(fname):
    "Output a dict of lines + char count for input file"
    f = open(fname)
    linecounts = [(line.strip(), len(line)) for line in f]
    f.close()
    return linecounts


def assembletweet(qf1, qf2):
    "Pick lines from each of q1 & q2 that sum to < TWEETSIZE chars"
    order = random.randrange(0, 2)
    if order > 0:
        q1 = parsequotes(qf1)
        q2 = parsequotes(qf2)
    else:
        q2 = parsequotes(qf1)
        q1 = parsequotes(qf2)
    # pick random quote from f1
    qdone = 0
    i = 0
    min2 = min(q2, key=lambda x: x[1])[1]
    for i in range(MAXTRIES):
        r1 = random.randrange(0, len(q1))
        if TWEETSIZE - q1[r1][1] - 1 > min2:
            break
    else:
        return None  # write some exception handling if loop can't pick short q1
    for i in range(MAXTRIES):
        r2 = random.randrange(0, len(q2))
        if TWEETSIZE - q1[r1][1] - 1 - q2[r2][1] >= 0:
            qdone = 1
            break
    else:
        return None  # more exception handling if loop can't pick short q2
    # Uppercase beginning of each quote
    t1 = q1[r1][0][0].upper() + q1[r1][0][1:len(q1[r1][0])]
    t2 = q2[r2][0][0].upper() + q2[r2][0][1:len(q2[r2][0])]
    # Check for punctuation at the end, add some if none.
    if t1.endswith(('?', ',', '.', '!')):
        pass
    else:
        t1 = t1 + '.'

    tweet = t1 + ' ' + t2
    return tweet

#Run the bot!
tweet = assembletweet(QUOTEF1, QUOTEF2)
if len(tweet) > 0:
    api.PostUpdates(tweet)