import pandas as pd
from datetime import timedelta

REPORTS_URL = 'https://safety2.oit.ncsu.edu//newblotter.asp'


def get_day(day):
    """Returns a dataframe of reports for a given date.

    Args:
        day: The Date to get reports for.

    Returns:
        A dataframe of police reports.
    """
    table = pd.read_html('https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE=10%2F09%2F23&submit=Submit')
    df = pd.concat(table)

    if len(df) > 1:
        new_header = df.iloc[1]
        df = df[1:]
        df.columns = new_header
        df = df.drop(0)
        df = df.astype(str)

        for index, row in df.iterrows():
            if row['Date / Time Occurred *'] == 'nan':
                row['Date / Time Occurred *'] = day.strftime(
                    '%x') + '  ' + row['Time Reported']
        return df


def get_range(start_date, end_date):
    """Returns a dataframe of reports for a date range.

    Args:
        start_date: The date to begin with.
        end_date: The date to end with (inclusive).

    Returns:
        A dataframe of police reports for a range of dates.
    """
    frames = list()
    delta = timedelta(days=1)
    while start_date <= end_date:
        df = get_day(start_date)
        if df is not None:
            frames.append(df)
        start_date += delta
    if frames[0] is not None:
        df = pd.concat(frames, ignore_index=True)
        return df
