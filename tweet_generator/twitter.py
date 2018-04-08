# author = rhnvrm <hello@rohanverma.net>

import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for the App
    '''
    def __init__(self, query, retweets_only=False, with_sentiment=False):
        # keys and tokens from the Twitter Dev Console
        #consumer_key = os.environ['QU2BhMy9th0YCufv29pUPYrns']
        consumer_key = 'QU2BhMy9th0YCufv29pUPYrns'
        #consumer_secret = os.environ['OFflhaTabnJBFtlmUtn97whTiDF7Cs6ElUVHy0q1MpPBgi0bbT']
        consumer_secret = 'OFflhaTabnJBFtlmUtn97whTiDF7Cs6ElUVHy0q1MpPBgi0bbT'
        #access_token = os.environ['1358275434-HuunDh25a0mN9QlwvPjbsAK5hI4o5v9NoIbyp5J']
        access_token = '1358275434-HuunDh25a0mN9QlwvPjbsAK5hI4o5v9NoIbyp5J'
        #access_token_secret = os.environ['Obbqg9AshVcfW2zw5wXarz6SxWg5BYJGXcN9DH8Y1gpzY']
        access_token_secret = 'Obbqg9AshVcfW2zw5wXarz6SxWg5BYJGXcN9DH8Y1gpzY'
        #print(os.environ['QU2BhMy9th0YCufv29pUPYrns'])
        # Attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.query = query
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100  # To prevent Rate Limiting
        except:
            print("Error: Authentication Failed")

    def set_query(self, query=''):
        self.query = query

    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self):
        tweets = []

        try:
            recd_tweets = self.api.search(q=self.query,
                                          count=self.tweet_count_max)
            if not recd_tweets:
                pass
            for tweet in recd_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name
                
                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
