import twitter
from datetime import datetime, timedelta
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

def getTweets(account='BBCNews', count=200, no_fetches=1):
    old_id = 0
    tweets = []
    for i in range(no_fetches):
        t = api.GetUserTimeline(screen_name=account, max_id=old_id, count=count, include_rts=1)
        new_tweets = [i.AsDict() for i in t]
        old_id = new_tweets[-1]['id']
        tweets += new_tweets
    if len(tweets) != count*no_fetches:
        print("Error:", len(tweets), "tweets")
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
    elif 'retweeted_status' in tweet:
        # Try retweeted tweet
        return getFavourites(tweet['retweeted_status'])
    else:
        return None

def getAccountName(tweet):
    """Get the account name of the original poster."""
    if 'retweeted_status' in tweet:
        return getAccountName(tweet['retweeted_status'])
    elif 'user' in tweet:
        return tweet['user']['name']
    else:
        return None

def getUrl(tweet):
    if len(tweet['urls']) > 0:
        return tweet['urls'][0]['url']
    elif 'retweeted_status' in tweet:
        # Try retweeted tweet
        return getUrl(tweet['retweeted_status'])
    else:
        return None

def formatTweetText(tweet_txt):
    result = tweet_txt
    result = re.sub(r' https.*', '', result)
    result = re.sub(r'\n.*', '', result)
    result = re.sub(r'^RT @.*: ', '', result)
    result += '.'
    return result

def createDataFrame(tweets):
    df = pd.DataFrame()

    for tweet in tweets:
        # Create datetime object
        date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")
        formatted_date = date.strftime("%d-%m-%Y")
        formatted_time = date.strftime("%X")
        
        account_name = getAccountName(tweet)
        no_favourites = getFavourites(tweet)
        url = getUrl(tweet)
        tweet_txt = formatTweetText(tweet['text'])
        
        # Filter tweets older than a week
        week_ago = datetime.now() - timedelta(days=7)
        if date.replace(tzinfo=None) > week_ago:
            df = df.append({'Account': account_name, 'Date': formatted_date, 'Time': formatted_time, 'Tweet': tweet_txt, 'Favourites': no_favourites, 'Retweets': tweet['retweet_count'], 'Url': url}, ignore_index=True)

    df.sort_values(by=['Favourites'], ascending=False, ignore_index=True, inplace=True)

    return df


api = getAPI()
tweets = getTweets(no_fetches=8)
saveTweets(tweets)

#tweets = loadTweets()

df = createDataFrame(tweets)
print(df.head(20))