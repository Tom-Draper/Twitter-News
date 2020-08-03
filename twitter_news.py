import twitter
from datetime import datetime
import re
import json
import pandas as pd
import pprint
import pickle

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)




def getAPI():
    # Read your twitter api details
    with open('my_api_details.json', 'r') as f:
        data = f.read()
    # Parse file
    obj = json.loads(data)

    api_key = obj['api-key']
    api_key_secret = obj['api-key-secret']
    access_token = obj['access-token']
    access_token_secret = obj["access-token-secret"]

    api = twitter.Api(consumer_key=api_key,
                      consumer_secret=api_key_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)
    return api

def getTweets(account='BBCNews', count=10):
    t = api.GetUserTimeline(screen_name=account, count=count)
    tweets = [i.AsDict() for i in t]
    return tweets

def saveTweets(tweets_list):
    with open('tweets.pickle', 'wb') as f:
        pickle.dump(tweets_list, f)

def loadTweets():
    with open('tweets.pickle', 'rb') as f:
        return pickle.load(f)

def getFavourites(tweet):
    if 'favorite_count' in tweet:
        return int(tweet['favorite_count'])
    else:
        return getFavourites(tweet['retweeted_status'])

def formatTweetText(tweet_txt):
    return re.sub(r'https.*', '', tweet_txt)

def createDataFrame(tweets):
    df = pd.DataFrame()

    for i, tweet in enumerate(tweets):
        print("TWEET", i)
        #pprint.pprint(tweet)
        
        # Create datetime object
        date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")
        formatted_date = date.strftime("%d-%m-%Y")
        formatted_time = date.strftime("%X")
        
        no_favourites = getFavourites(tweet)
        tweet_txt = formatTweetText(tweet['text'])
    
    df = df.append({'Date': formatted_date, 'Time': formatted_time, 'Tweet': tweet_txt, 'Favourites': no_favourites, 'Retweets': tweet['retweet_count']}, ignore_index=True)

    df.sort_values(by=['Favourites'], ascending=False, ignore_index=True, inplace=True)

    return df

#api = getAPI()
#tweets = getTweets(count=100)
#saveTweets(tweets)
tweets = loadTweets()
print(len(tweets))

df = createDataFrame(tweets)
