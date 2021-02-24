import tweepy
from tweepy import OAuthHandler

LIMIT = 200


class Twitter(object):
    """
    Twitter class for tweet extraction and preprocessing
    """

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        api_key = ***REMOVED***
        api_secret = ***REMOVED***
        access_token = ***REMOVED***
        access_token_secret = ***REMOVED***

        # create OAuthHandler object
        self.auth = OAuthHandler(api_key, api_secret)

        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)

        # create tweepy API object to fetch tweets
        self.api = tweepy.API(self.auth, wait_on_rate_limit=False)

    def get_tweets(self, query, count):
        # store processed tweet data dicts in list
        tweet_id_num_batch = []
        calls = 0

        while count > 0:
            if count >= LIMIT:
                # if still need more than limit, get limit
                single_call = self.api.search(q=query, count=LIMIT, lang='en',result_type='recent',wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
            else:
                # if need less the limit, get what is left
                single_call = self.api.search(q=query, count=count,lang='en',result_type='recent',wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

            count -= LIMIT
            calls += 1

            # for tweets in batch, get full text and process tweets
            for single_tweet in single_call:
                tweet_id = single_tweet.id
                tweet_id_num_batch.append(str(tweet_id))

        return tweet_id_num_batch

    def get_dependency_tweets(self, query_list, count):
        tweet_id_list = []
        num = 0

        # keep pulling tweets until reach needed count
        while len(tweet_id_list) != count:
            # circular index of query_list
            if num < len(query_list):
                index = num
            else:
                index = num % len(query_list)

            # pull tweet id batch, add to list
            tweet_ids = self.get_tweets(query_list[index], 7)
            if len(tweet_ids) != 0:
                for the_tweet_id in tweet_ids:
                    if the_tweet_id is not tweet_id_list:
                        tweet_id_list.append(the_tweet_id)
                    if len(tweet_id_list) == count:
                        break

            num += 1
        print(num)
        return tweet_id_list
