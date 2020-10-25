import twitter
from datetime import datetime, timedelta
import re
import json
import pandas as pd
import pickle
from send_emails import EmailSender

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class TwitterNews:
    def __init__(self):
        self.api = self.getAPI()
    
    def getAPI(self):
        # Read your twitter api details
        with open('api_details.json', 'r') as f:
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

    def getTweets(self, account='BBCNews', count=200, no_fetches=1):
        old_id = 0
        tweets = []
        for i in range(no_fetches):
            t = self.api.GetUserTimeline(screen_name=account, max_id=old_id, count=count, include_rts=1)
            new_tweets = [i.AsDict() for i in t]
            old_id = new_tweets[-1]['id']
            tweets += new_tweets
        if len(tweets) != count*no_fetches:
            print("Error:", len(tweets), "tweets")
        return tweets

    def saveTweets(self, tweets_list):
        with open('tweets.pickle', 'wb') as f:
            pickle.dump(tweets_list, f)

    def loadTweets(self):
        with open('tweets.pickle', 'rb') as f:
            return pickle.load(f)

    def getFavourites(self, tweet):
        if 'favorite_count' in tweet:
            return tweet['favorite_count']
        elif 'retweeted_status' in tweet:
            # Try retweeted tweet
            return self.getFavourites(tweet['retweeted_status'])
        else:
            return None

    def getAccountName(self, tweet):
        """Get the account name of the original poster."""
        if 'retweeted_status' in tweet:
            return self.getAccountName(tweet['retweeted_status'])
        elif 'user' in tweet:
            return tweet['user']['name']
        else:
            return None

    def getUrl(self, tweet):
        if len(tweet['urls']) > 0:
            return tweet['urls'][0]['url']
        elif 'retweeted_status' in tweet:
            # Try retweeted tweet
            return self.getUrl(tweet['retweeted_status'])
        else:
            return None

    def formatTweetText(self, tweet_txt):
        result = tweet_txt
        result = re.sub(r' https.*', '', result)
        result = re.sub(r'\n.*', '', result)
        result = re.sub(r'^RT @.*: ', '', result)
        return result

    def createDataFrame(self, tweets):
        df = pd.DataFrame()

        for tweet in tweets:
            # Create datetime object
            date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")
            formatted_date = date.strftime("%d/%m/%Y")
            formatted_time = date.strftime("%X")
            
            account_name = self.getAccountName(tweet)
            no_favourites = self.getFavourites(tweet)
            url = self.getUrl(tweet)
            tweet_txt = self.formatTweetText(tweet['text'])
            if 'retweet_count' in tweet.keys():
                retweets = tweet['retweet_count']
            else:
                retweets = 0
            
            # Filter tweets older than a week
            week_ago = datetime.now() - timedelta(days=7)
            if date.replace(tzinfo=None) > week_ago:
                df = df.append({'Account': account_name, 'Date': formatted_date, 'Time': formatted_time, 'Tweet': tweet_txt, 'Favourites': no_favourites, 'Retweets': retweets, 'Url': url}, ignore_index=True)

        # Sort by descending number of likes
        df.sort_values(by=['Favourites'], ascending=False, ignore_index=True, inplace=True)

        return df
    
    def createEmailBodyPlain(self, df):
        now = datetime.now().strftime("%d/%m/%y")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%y")
        
        # Build email body text
        text = f'Weekly News: {week_ago} - {now}\n'
        text += "-"*len(text)*1.5 + "\n\n"
        for row in df.itertuples():
            account_and_time = f"{row.Account} -- {str(row.Date)} at {str(row.Time)}"
            tweet_text = f"{row.Tweet}"
            fav_and_retweets = f"Favourites: {int(row.Favourites)}  Retweets: {int(row.Retweets)}"
            url = str(row.Url)
            
            news_article = account_and_time + '\n' + tweet_text + '\n' \
                                       + fav_and_retweets + '\n' + url
            text += news_article + '\n\n'
        
        return text

    def createEmailBodyHTML(self, df):
        now = datetime.now().strftime("%d/%m/%y")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%y")
        
        # Build email body text
        text = f'<h3><u>Weekly News: {week_ago} - {now}</u></h3>'
        for row in df.itertuples():
            account_and_time = f"{row.Account} -- {str(row.Date)} at {str(row.Time)}"
            tweet_text = f"{row.Tweet}"
            fav_and_retweets = f"Favourites: {int(row.Favourites)} &ensp; Retweets: {int(row.Retweets)}"
            url = str(row.Url)
            
            news_article = account_and_time + '<br>' + '<b>' + tweet_text + '</b>' \
                           + '<br>' + fav_and_retweets + '<br>' + url
            text += news_article + '<br><br>'
        
        return text

    def main(self, no_tweets=10):
        # Get tweets
        print("Fetching tweets...")
        tweets = self.getTweets(no_fetches=6)
        self.saveTweets(tweets)
        #tweets = loadTweets()
        
        # Make sorted dataframe of top tweets
        df = self.createDataFrame(tweets)
        print(df.head(no_tweets))
        
        # Send emails
        email_body = self.createEmailBodyHTML(df.head(no_tweets))
        print("\nEmail body will be as follows:\n")
        print(email_body.replace('<br>', '\n'))
        sender = EmailSender()
        sender.sendEmails("Weekly News", body=email_body, body_type='html')


if __name__ == "__main__":
    tn = TwitterNews()
    tn.main()