from db import insert_report


def create_tweets_from_text_helper(text: str, tweets: list):
    if len(text) <= 280:
        return tweets.append(text)

    tweets.append(text[:277] + "\u2026")
    return create_tweets_from_text_helper("\u2026" + text[277:], tweets)


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


def tweet_report(client, report):
    tweets = create_tweets_from_report(report)
    response = client.create_tweet(text=tweets[0])

    for reply in tweets[1:]:
        response = client.create_tweet(
            text=reply, in_reply_to_tweet_id=response.data["id"]
        )
    insert_report(report)
