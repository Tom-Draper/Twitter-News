# Twitter-News

An emailing system that sends emails containing the top most favourited tweets/retweets from a news media Twitter account to a mailing list.

## Getting Started
### Setup
1. Enter your Twitter API:
- API key
- API key secret
- access token
- access token secret
into the appropriate places in the api_details.json file.
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

### Sending
Run the twitter_news.py file to send the top news tweets from the past week to each email listed in the mailing list inside the email_details.json file.
