from datetime import date
from pandas import DataFrame
from tweepy import Client
from db import insert_report, report_exists
from scraper import scrape_days


def create_tweets_from_text_helper(text: str, tweets: list):
    MAX_TWEET_LENGTH = 280
    if len(text) <= MAX_TWEET_LENGTH:
        return tweets.append(text)

    tweets.append(text[: MAX_TWEET_LENGTH - 1] + "⋯")
    return create_tweets_from_text_helper("⋯" + text[MAX_TWEET_LENGTH - 1 :], tweets)


def create_tweets_from_text(text: str) -> list:
    tweets = []
    create_tweets_from_text_helper(text, tweets)
    return tweets


def create_tweets_from_report(report: DataFrame) -> list:
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


def tweet_reports(start_date: date, end_date: date, client: Client) -> None:
    reports = scrape_days(start_date, end_date)

    if reports is None:
        return

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
