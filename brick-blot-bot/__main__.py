import tweepy
from os import environ
from datetime import date, timedelta
from dotenv import load_dotenv

from tweets import tweet_reports


load_dotenv()

client = tweepy.Client(
    consumer_key=environ.get("CONSUMER_KEY"),
    consumer_secret=environ.get("CONSUMER_KEY_SECRET"),
    access_token=environ.get("ACCESS_TOKEN"),
    access_token_secret=environ.get("ACCESS_TOKEN_SECRET"),
)

tweet_reports(date.today() - timedelta(30), date.today(), client)
