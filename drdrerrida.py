# This script pulls random lyrics/quotes from two files
# and mashes them together to make one <140 character tweet

import random
import sys
from time import sleep
import socket
import logging
import twitter
import yaml


class Quotemasher:

    def __init__(self, quotes1, quotes2):
        """ Be sure to pass quotes1/quotes2 in a random order!

        :param quotes1:
        :param quotes2:
        :return:
        """
        self.quotes1 = quotes1
        self.quotes2 = quotes2

    def buildTweet(self, tweetsize):
        """ Pick lines from each quote list that sum to < tweetsize chars
        :return: tweet text
        """
        try:
            q1 = random.choice(filter(lambda x: len(x) < tweetsize - 1, self.quotes1))
        except IndexError:
            # nothing in quotes1 is shorter than tweetsize!
            return None

        try:
            len2 = tweetsize - len(q1) - 2
            q2 = random.choice(filter(lambda x: len(x) < len2, self.quotes2))
        except IndexError:
            # q1 is too long for any of the quotes in q2, that's ok, just tweet it alone
            q2 = ''

        if random.randrange(0, 2) > 0:
            tweet = q1 + ' ' + q2
        else:
            tweet = q2 + ' ' + q1

        #check for punctuation at the end, add some if none
        if tweet.endswith(('?', ',', '.', '!')):
            pass
        else:
            tweet += '.'

        return tweet


def run_drdrerrida(rootdir):

    drefile = rootdir + 'dre_quotes.txt'
    derridafile = rootdir + 'derrida_quotes.txt'

    with open(drefile) as f:
        drequotes = [line.strip() for line in f]
    with open(derridafile) as f:
        derridaquotes = [line.strip() for line in f]

    twitter_tokens = yaml.load(open(rootdir + 'config.yaml'))
    api = twitter.Api(**twitter_tokens)

    while True:
        if random.randrange(0, 2) > 0:
            q = Quotemasher(drequotes, derridaquotes)
        else:
            q = Quotemasher(derridaquotes, drequotes)

        tweet = q.buildTweet(140)

        try:
            api.PostUpdate(tweet)
        except twitter.TwitterError:
            pass

        sleep(random.randrange(6666, 9999))


if __name__ == '__main__':
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    lock_id = "mcmoots.drdrerrida"
    try:
        lock_socket.bind('\0' + lock_id)
        logging.debug("Got lock %r" % (lock_id,))
    except socket.error:
        # socket already locked, task must be running
        logging.info("Failed to get lock %r" % (lock_id,))
        sys.exit()

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = './'

    run_drdrerrida(root)