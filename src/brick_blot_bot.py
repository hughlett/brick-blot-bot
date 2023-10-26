import tweepy
from os import environ
from datetime import date, timedelta
from dotenv import load_dotenv
from db import insert_report, report_exists
from scraper import scrape_days
from messages import create_message_from_report

def main():
    load_dotenv()

    auth = tweepy.OAuthHandler(environ.get('API'), environ.get('API_SECRET'))
    auth.set_access_token(environ.get('ACCESS_TOKEN'), environ.get('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)

    df = scrape_days(date.today() - timedelta(30), date.today())
    if df is None:
        return
    
    for index, row in df.iterrows():
        if not report_exists(row['Report Number']):
            insert_report(row)
            message = create_message_from_report(row)

            try:
                status = api.update_status(message[0])
                for reply in message[1:]:
                    status = api.update_status(reply, status.id)
            except tweepy.TweepError:
                pass        

if __name__ == "__main__":
    main()
