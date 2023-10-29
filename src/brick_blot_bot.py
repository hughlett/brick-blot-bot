import tweepy
from os import environ
from datetime import date, timedelta
from dotenv import load_dotenv
from db import create_table, insert_report, report_exists
from scraper import scrape_days
from messages import create_message_from_report


def main():
    load_dotenv()
    create_table()

    client = tweepy.Client(
        consumer_key=environ.get("API"),
        consumer_secret=environ.get("API_SECRET"),
        access_token=environ.get("ACCESS_TOKEN"),
        access_token_secret=environ.get("ACCESS_TOKEN_SECRET"),
    )

    df = scrape_days(date.today() - timedelta(30), date.today())
    if df is None:
        return

    MAX_API_CALLS = 50
    api_calls = 0

    for index, row in df.iterrows():
        if not report_exists(row["Report Number"]):
            message = create_message_from_report(row)

            if api_calls + len(message) <= MAX_API_CALLS:
                api_calls += len(message)
                insert_report(row)
                response = client.create_tweet(text=message[0])
                for reply in message[1:]:
                    response = client.create_tweet(
                        text=reply, in_reply_to_tweet_id=response.data["id"]
                    )


if __name__ == "__main__":
    main()
