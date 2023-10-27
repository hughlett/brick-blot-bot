from io import StringIO
import pandas as pd
from datetime import timedelta
import requests

def scrape_day(date):
    print(date)
    url = f"https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE={date.month}%2F{date.day}%2F{date.year % 100}&submit=Submit"
    html = requests.get(url).text
    df = pd.read_html(StringIO(html))

    if len(df) > 1:
        df = df[1]
        df = df.rename(columns=df.iloc[0]) # Rename columns
        df = df.drop(df.index[0]) # Drop first row that containers column headers
        df = df.iloc[:, :-1] # Drop Disposition column
        df['Date / Time  Occurred *'] = df['Date / Time  Occurred *'].fillna(date.strftime('%x')) # Add date

        return df
    
    return None

def scrape_days(start_date, end_date):
    dataframes = list()
    delta = timedelta(days=1)

    while start_date <= end_date:
        reports = scrape_day(start_date)
        if reports is not None: dataframes.append(reports)
        start_date += delta

    if dataframes[0] is not None:
        return pd.concat(dataframes, ignore_index=True)
