import tweepy
from tweepy import OAuthHandler
import random
import requests
import sys
sys.dont_write_bytecode = True
LIMIT = 350

class Twitter(object):
    """
    Twitter class for tweet extraction and preprocessing
    """

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = ***REMOVED***
        consumer_secret = ***REMOVED***
        access_token = ***REMOVED***
        access_token_secret = ***REMOVED***

        # create OAuthHandler object
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)

        # create tweepy API object to fetch tweets
        self.api = tweepy.API(self.auth)

        self.tweet_id_dict = None

    def get_text(self, tweet):
        # get full text of tweet
        if 'RT ' in tweet.full_text[0:4]:
            tweet_text = tweet.retweeted_status.full_text
        else:
            tweet_text = tweet.full_text

        return tweet_text

    def get_tweets(self, query, count):
        #query += ' -filter:retweets'
        print(query)
        single_call = self.api.search(q=query, count=count, tweet_mode='extended', lang='en')

        # for tweets in batch, get full text and process tweets
        tweet_text = []
        tweet_ids = []
        for single_tweet in single_call:
            print(single_tweet.id)
            full_tweet = self.api.get_status(single_tweet.id, tweet_mode='extended')
            tweet_text.append(full_tweet.full_text)
            tweet_ids.append(single_tweet.id)

        id_text_dict = {}
        for id, text in zip(tweet_ids, tweet_text):
            if text not in id_text_dict.values():
                id_text_dict[id] = text

        return id_text_dict

    def combine_tweet_dicts(self,list_of_dicts):
        combined = list_of_dicts.pop()
        while len(list_of_dicts) != 0:
            next_dict = list_of_dicts.pop()
            combined = {**combined, **next_dict}

        unique_dict = {}
        for id, text in combined.items():
            if text not in unique_dict.values():
                unique_dict[id] = text

        return unique_dict

    def filter_tweet_batch(self):
        # given tweet text list, try to filter out irrelevant data
        print('something')

    def sort_by_severity(self, id_text_dict):
        # Dian's classifier
        tweets = []
        for id, text in id_text_dict.items():
            tweets.append((text,id))

        url = "http://0.0.0.0:9802/tweet/pred"
        query = {"tweets": tweets}
        pred = requests.post(url=url, json=query)

        # iterate through list, match text to id, append to list
        print('pred: ', pred)
        list_of_dicts = pred.json()
        filtered_dict = {}
        for tweet_obj in list_of_dicts:
            text = tweet_obj['text']
            id = str(tweet_obj['id'])
            filtered_dict[id] = text

        return filtered_dict

    def get_query(self, query_list):
        queries = []
        for query_item in query_list:
            exact_match = '\"'+ query_item + '\"'
            no_space = '\"'+ query_item.replace(' ','') + '\"'
            if exact_match != no_space:
                queries.extend([exact_match, no_space])
            else:
                queries.extend([exact_match])

        query = ''
        for i in range(len(queries) - 1):
            if i == 0:
                query += '( ' + queries[i]
            else:
                query += ' OR ' + queries[i]
        query += ' ) ' + '( ' + 'vulnerability' + ' OR ' + ' ddos' + ' )'
        
        return query
