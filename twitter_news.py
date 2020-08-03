import twitter
from datetime import datetime
import json
import pandas as pd
import pprint

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

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



def getFavourites(tweet):
    print(type(tweet))
    return 1


t = api.GetUserTimeline(screen_name='BBCNews', count=5)
tweets = [i.AsDict() for i in t]
df = pd.DataFrame()

for i, tweet in enumerate(tweets):
    print("TWEET", i)
    pprint.pprint(tweet)
    # Create datetime object
    date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")
    formatted_date = date.strftime("%d-%m-%Y")
    formatted_time = date.strftime("%X")
    no_favourites
    
    df = df.append({'Date': formatted_date, 'Time': formatted_time, 'Tweet': tweet['text'], 'Favourites': no_favourites, 'Retweets': tweet['retweet_count']}, ignore_index=True)

print(df)