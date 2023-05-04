import tweepy
from os import environ
from datetime import date, timedelta
from src.scraper import get_range
from src.messages import get_reports_as_messages

auth = tweepy.OAuthHandler(environ['API'], environ['API_SECRET'])
auth.set_access_token(environ['ACCESS_TOKEN'], environ['ACCESS_TOKEN_SECRET'])
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
