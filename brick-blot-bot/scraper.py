from io import StringIO
from pandas import read_html, concat, DataFrame
from datetime import date, timedelta
import requests


def scrape_day(date: date) -> DataFrame:
    url = f"https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE={str(date.month).zfill(2)}%2F{str(date.day).zfill(2)}%2F{date.year % 100}&submit=Submit"
    html = requests.get(url).text
    df = read_html(StringIO(html))

    if len(df) <= 1:
        return None

    df = df[1]
    df = df.rename(columns=df.iloc[0])  # Rename columns
    df = df.drop(df.index[0])  # Drop first row that containers column headers
    df = df.iloc[:, :-1]  # Drop Disposition column
    df["Date / Time  Occurred *"] = df["Date / Time  Occurred *"].fillna(
        date.strftime("%x")
    )  # Add date

    return df


def scrape_days(start_date: date, end_date: date) -> DataFrame | None:
    dataframes = list()
    delta = timedelta(days=1)

    while start_date <= end_date:
        reports = scrape_day(start_date)
        if reports is not None:
            dataframes.append(reports)
        start_date += delta

    if not dataframes:
        return None

    return concat(dataframes, ignore_index=True)
