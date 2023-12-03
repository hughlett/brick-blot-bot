from datetime import date
from os import environ
from create_tweet import create_tweets_from_report
import tweepy
from db import insert_report, report_exists
from scrape_reports import scrape_days


def tweet_reports(start_date: date, end_date: date) -> None:
    """Post police reports over a range of dates.

    Args:
        start_date (date):
        end_date (date):
    """
    reports = scrape_days(start_date, end_date)

    if reports is None:
        return

    client = tweepy.Client(
        consumer_key=environ.get("CONSUMER_KEY"),
        consumer_secret=environ.get("CONSUMER_KEY_SECRET"),
        access_token=environ.get("ACCESS_TOKEN"),
        access_token_secret=environ.get("ACCESS_TOKEN_SECRET"),
        wait_on_rate_limit=True,
    )

    API_RATE_LIMIT = 50
    api_calls_made = 0

    for index, report in reports.iterrows():
        if report_exists(report["Report Number"]):
            continue

        tweets = create_tweets_from_report(report)

        if api_calls_made + len(tweets) >= API_RATE_LIMIT:
            return

        api_calls_made += len(tweets)
        response = client.create_tweet(text=tweets[0])

        for reply in tweets[1:]:
            response = client.create_tweet(
                text=reply, in_reply_to_tweet_id=response.data["id"]
            )
        insert_report(report)
