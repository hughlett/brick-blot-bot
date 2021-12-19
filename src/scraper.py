import platform
import sys
import pandas as pd
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

REPORTS_URL = 'https://safety2.oit.ncsu.edu//newblotter.asp'
CHROME_URL = 'http://127.0.0.1:4444/wd/hub'


def make_driver():
    """Returns a selenium webdriver.

    Returns:
        A webdriver for either a Windows Chrome install
        or a remote instance of Chrome on localhost:4444.
    """
    options = Options()
    options.headless = True
    os = platform.system()

    if os == 'Linux':
        return webdriver.Remote(CHROME_URL, DesiredCapabilities.CHROME, options=options)
    elif os == 'Windows':
        return webdriver.Chrome('./chromedriver', options=options)
    else:
        print(f'scraper.py does not support {os}.')
        sys.exit()


def get_day(day, driver):
    """Returns a dataframe of reports for a given date.

    Args:
        day: The Date to get reports for.
        driver: The webdriver to use.

    Returns:
        A dataframe of police reports.
    """
    close_driver = False
    if driver == None:
        driver = make_driver()
        close_driver = True
    driver.get(REPORTS_URL)
    driver.set_page_load_timeout(20)

    search_box = driver.find_element_by_xpath('//*[@id="NOTDATE"]')
    submit = driver.find_element_by_xpath('/html/body/form/p[1]/input[2]')
    search_box.clear()
    search_box.send_keys(str(day.strftime("%x")))
    submit.click()

    table = pd.read_html(driver.current_url)
    df = pd.concat(table)

    if close_driver:
        driver.quit()

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
    driver = make_driver()
    delta = timedelta(days=1)
    while start_date <= end_date:
        df = get_day(start_date, driver)
        if df is not None:
            frames.append(df)
        start_date += delta
    driver.quit()
    if frames[0] is not None:
        df = pd.concat(frames, ignore_index=True)
        return df
