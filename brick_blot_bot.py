import tweepy
from os import environ
from os.path import dirname, abspath, join
from datetime import date, timedelta
from dotenv import load_dotenv
from src.scraper import get_range
from src.messages import get_reports_as_messages

PATH_TO_KEYS = abspath(dirname(abspath(__file__)))

load_dotenv(join(PATH_TO_KEYS, '.env'))
auth = tweepy.OAuthHandler(environ['API'], environ['APISecret'])
auth.set_access_token(environ['AccessToken'], environ['AccessTokenSecret'])
api = tweepy.API(auth)


def main():
    df = get_range(date.today() - timedelta(7), date.today())
    if df is None:
        return

    messages = get_reports_as_messages(df)
    old_statuses = api.user_timeline(
        'brickblotbot', count=150, tweet_mode='extended')
    old_messages = list()
    for status in old_statuses:
        old_messages.append(status.full_text.replace('&amp;', '&'))

    for message in messages:
        if message[0] not in old_messages:
            try:
                status = api.update_status(message[0])
                for reply in message[1:]:
                    status = api.update_status(reply, status.id)
            except tweepy.TweepError:
                pass


if __name__ == "__main__":
    main()
