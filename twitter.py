import tweepy
from tweepy import OAuthHandler

LIMIT = 200


class Twitter(object):
    """
    Twitter class for tweet extraction and preprocessing
    """

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'OONxxHdjTdGnJnnJ8Kg6d14bP'
        consumer_secret = 'aZLkk2AV6RPqyxaDrCv3tOxyivP9yC1hhFpUJ2cOYEvej2WaAS'
        access_token = '1300638328404934659-BuDxv7e45rHhx1mkKfUQ1V2Dto17Ca'
        access_token_secret = 'vkmBTyC1OJNFP7bTF2QPrH7sVZgNPwzYGceCLC7DPmqhN'

        # create OAuthHandler object
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)

        # create tweepy API object to fetch tweets
        self.api = tweepy.API(self.auth)


    def get_tweets(self, query, count):
        # store processed tweet data dicts in list
        tweet_id_num_batch = []
        calls = 0

        while count > 0:
            if count >= LIMIT:
                # if still need more than limit, get limit
                single_call = self.api.search(q=query, count=LIMIT, tweet_mode='extended', lang='en',result_type='recent')
            else:
                # if need less the limit, get what is left
                single_call = self.api.search(q=query, count=count,lang='en',result_type='recent')

            count -= LIMIT
            calls += 1

            # for tweets in batch, get full text and process tweets
            for single_tweet in single_call:
                tweet_id = single_tweet.id
                tweet_id_num_batch.append(str(tweet_id))

        return tweet_id_num_batch
