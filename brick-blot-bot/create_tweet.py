from pandas import Series


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
    return create_tweets_from_text_helper(
        "..." + text[MAX_TWEET_LENGTH - len(ellipsis) :], tweets
    )


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
