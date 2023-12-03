from datetime import date
from os import environ
from pandas import Series
import tweepy
from db import insert_report, report_exists
from scraper import scrape_days


def create_tweets_from_text_helper(text: str, tweets: list):
    """_summary_

    Args:
        text (str): _description_
        tweets (list): _description_

    Returns:
        _type_: _description_
    """
    MAX_TWEET_LENGTH = 280  # https://developer.twitter.com/en/docs/counting-characters
    ellipsis = "..."

    if len(text) <= MAX_TWEET_LENGTH:
        return tweets.append(text)

    tweets.append(text[: MAX_TWEET_LENGTH - len(ellipsis)] + ellipsis)
    return create_tweets_from_text_helper("⋯" + text[MAX_TWEET_LENGTH - 1 :], tweets)


def create_tweets_from_text(text: str) -> list:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        list: _description_
    """
    # TODO: Look into verifying the final tweet with https://github.com/twitter/twitter-text/tree/master/js
    tweets = []
    create_tweets_from_text_helper(text, tweets)
    return tweets


def create_tweets_from_report(report: Series) -> list:
    """_summary_

    Args:
        report (DataFrame): _description_

    Returns:
        list: _description_
    """
    date_and_time = report["Date / Time  Occurred *"].split("  ")
    date = date_and_time[0]

    time = report["Time Reported"] if len(date_and_time) == 1 else date_and_time[1]

    text = (
        report["Location"]
        + "\n"
        + date
        + " "
        + time
        + "\n"
        + report["Incident"]
        + "\n"
        + "\n"
        + report["Narrative"]
    )
    return create_tweets_from_text(text)


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
