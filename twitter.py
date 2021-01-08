import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

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

    def clean_tweet(self, tweet):
        # remove special chars, links, and @usernames
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+) ", " ", tweet).split())

    def get_sentiment(self, tweet):
        # get sentiment index between -1 and 1
        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity

        # get sentiment
        if polarity > 0.0:
            sentiment = 'positive'
        elif polarity == 0.0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'

        return sentiment, polarity

    def get_data(self, tweet):
        # dict of tweet data
        tweet_data = {}

        # get full text of tweet
        if 'RT ' in tweet.full_text[0:4]:
            tweet_data['text'] = tweet.retweeted_status.full_text
        else:
            tweet_data['text'] = tweet.full_text

        tweet_data['text'] = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet_data['text'], flags=re.MULTILINE)

        # get list of separated words in tweet
        tweet_data['word_list'] = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+) ", " ",
                                         tweet_data['text']).lower().split()
        special_free = [word for word in tweet_data['word_list'] if word.isalnum()]
        tweet_data['word_list'] = special_free

        # get language to make sure can analyze english-only
        tweet_data['lang'] = tweet.lang

        # get sentiment of tweet
        tweet_data['sentiment'], tweet_data['polarity'] = self.get_sentiment(' '.join(tweet_data['word_list']))

        return tweet_data

    def get_tweets(self, query, count):
        # store processed tweet data dicts in list
        processed_tweets = []
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
            tweet_batch = []
            for single_tweet in single_call:
                full_tweet = self.api.get_status(single_tweet.id, tweet_mode='extended')
                tweet_batch.append(self.get_data(full_tweet))
            processed_tweets.extend(tweet_batch)
        return processed_tweets
