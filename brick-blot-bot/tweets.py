from datetime import date, timedelta
from db import insert_report, report_exists
from scraper import scrape_days


def create_tweets_from_text_helper(text: str, tweets: list):
    MAX_TWEET_LENGTH = 280
    if len(text) <= MAX_TWEET_LENGTH:
        return tweets.append(text)

    tweets.append(text[: MAX_TWEET_LENGTH - 3] + "\u2026")
    return create_tweets_from_text_helper(
        "\u2026" + text[MAX_TWEET_LENGTH - 3 :], tweets
    )


def create_tweets_from_text(text: str):
    tweets = []
    create_tweets_from_text_helper(text, tweets)
    return tweets


def create_tweets_from_report(report):
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


def tweet_reports(start_date, end_date, client):
    df = scrape_days(start_date, end_date)

    if df is None:
        return

    MAX_API_CALLS = 50
    api_calls = 0

    for index, report in df.iterrows():
        if report_exists(report["Report Number"]):
            continue

        tweets = create_tweets_from_report(report)

        if api_calls + len(tweets) >= MAX_API_CALLS:
            return

        api_calls += len(tweets)
        response = client.create_tweet(text=tweets[0])

        for reply in tweets[1:]:
            response = client.create_tweet(
                text=reply, in_reply_to_tweet_id=response.data["id"]
            )
        insert_report(report)
