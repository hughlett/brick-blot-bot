import tweepy
from os import environ
from datetime import date, timedelta
from dotenv import load_dotenv
from db import create_table, insert_report, report_exists
from scraper import scrape_days
from tweets import create_tweets_from_report, tweet_report


def main():
    load_dotenv()
    # create_table()

    client = tweepy.Client(
        consumer_key=environ.get("API"),
        consumer_secret=environ.get("API_SECRET"),
        access_token=environ.get("ACCESS_TOKEN"),
        access_token_secret=environ.get("ACCESS_TOKEN_SECRET"),
    )

    df = scrape_days(date.today() - timedelta(30), date.today())
    if df is None:
        return

    for index, row in df.iterrows():
        if not report_exists(row["Report Number"]):
            tweet_report(client, row)


if __name__ == "__main__":
    main()
