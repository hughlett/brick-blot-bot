import os
from datetime import date, timedelta
from dotenv import load_dotenv
from tweets import tweet_reports

if "GITHUB_ACTION" not in os.environ:
    load_dotenv(".env")

tweet_reports(date.today() - timedelta(30), date.today())
