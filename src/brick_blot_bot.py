import tweepy
from os import environ
from os.path import dirname, abspath, join
from dotenv import load_dotenv
from scraper import get_range, get_yesterday, get_day
from datetime import date, timedelta
from messages import get_reports_as_messages

PATH_TO_KEYS = abspath(dirname(dirname(abspath(__file__))))

load_dotenv(join(PATH_TO_KEYS, '.env'))
auth = tweepy.OAuthHandler(environ['API'], environ['APISecret'])
auth.set_access_token(environ['AccessToken'], environ['AccessTokenSecret'])
api = tweepy.API(auth)

def main():
    df = get_range(date.today() - timedelta(3), date.today())
    if df is None:
        return

    messages = get_reports_as_messages(df)
    for message in messages:
        try:
            status = api.update_status(message[0])
            for reply in message[1:]:
                status = api.update_status(reply, status.id)
        except tweepy.TweepError as e:
            pass
if __name__=="__main__":
    main()