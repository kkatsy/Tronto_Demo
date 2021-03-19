import tweepy
from tweepy import OAuthHandler

LIMIT = 200


class Twitter(object):
    """
    Twitter class for tweet extraction and preprocessing
    """

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        api_key = 'EBoeQqGvXzEELZ1yK6f3sqkOI'
        api_secret = 'YRVYcmQMcoUs4324d9AKJ0YTG4YznnkJtRD8yG1XrqrqGmrxtx'
        access_token = '1300638328404934659-z6Z8qJGi8JZNjNbnYlOBsqMJA2DMQg'
        access_token_secret = 'cJa52zlCLoZC2DMiJIqYn4dCYFIPE34j748DkgsIrgcqy'

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
        tweet_id_list = ['1370848573391130624', '1370848524854644738', '1371894313609756679', '1371866105472516101', '1371865931207561217', '1371865263512113160', '1372029510980354053', '1372017400120479744', '1371020318588932097', '1370587503107960835','1372698079070146566', '1372698068605231104', '1372696051816235014', '1372695929334161419', '1372688609652961280']

        return tweet_id_list
