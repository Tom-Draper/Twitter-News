# Twitter-News

An emailing system that sends the top most favourited tweets and retweets from a news media Twitter account over the past week to a mailing list. The default account is the BBCNews Twitter account.

## Getting Started
### Set up and Config
1. Enter the following into the appropriate places in the api_details.json file from your Twitter API access:
- API key;
- API key secret;
- access token;
- access token secret.
2. Enter your sending Gmail account details into the appropriate places in the email_details.json file.
3. Enter the emails of your mailing list into the appropriate place in the email_details.json file. 
4. Ensure your Gmail account account has "less secure app access" enabled in your Google account settings.

### Prerequisites
py -m pip install:
- smtplib
- twitter-python
- re
- pickle
- pandas
- json

### Sending Emails
Run the twitter_news.py file to send the top news tweets from the past week to each email listed in the mailing list inside the email_details.json file.
