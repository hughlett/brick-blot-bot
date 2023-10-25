from time import sleep
import tweepy
from os import environ
from datetime import date, timedelta
from dotenv import load_dotenv
from scraper import get_range
from messages import get_reports_as_messages
import pandas as pd
import requests

def main():
    # load_dotenv()

    # auth = tweepy.OAuthHandler(environ.get('API'), environ.get('API_SECRET'))
    # auth.set_access_token(environ.get('ACCESS_TOKEN'), environ.get('ACCESS_TOKEN_SECRET'))
    # api = tweepy.API(auth)

    html = requests.get('https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE=10%2F16%2F23&submit=Submit').text
    df = pd.read_html(html)[1]
    print(df.iloc[1][0])

    # table = pd.read_html('https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE=10%2F09%2F23&submit=Submit', encoding='UTF-8')
    # df = pd.concat(table)
    # print(df)


    # df = get_range(date.today() - timedelta(7), date.today())
    # if df is None:
    #     return

    # messages = get_reports_as_messages(df)
    # old_statuses = api.user_timeline(
    #     'brickblotbot', count=150, tweet_mode='extended')
    # old_messages = list()
    # for status in old_statuses:
    #     old_messages.append(status.full_text.replace('&amp;', '&'))

    # for message in messages:
    #     if message[0] not in old_messages:
    #         try:
    #             status = api.update_status(message[0])
    #             for reply in message[1:]:
    #                 status = api.update_status(reply, status.id)
    #         except tweepy.TweepError:
    #             pass

if __name__ == "__main__":
    main()
