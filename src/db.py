import sqlite3
import pandas as pd

import requests

connection = sqlite3.connect("reports.db")

# Create table
cursor = connection.cursor()
# cursor.execute("CREATE TABLE report (report_number INTEGER, time_reported TEXT, date_time_occurred TEXT, incident TEXT, location TEXT, narrative TEXT)")

# Insert a row
html = requests.get('https://safety2.oit.ncsu.edu/newblotter.asp?NOTDTE=10%2F16%2F23&submit=Submit').text
df = pd.read_html(html)[1]
cursor.execute("INSERT INTO report (report_number, time_reported, date_time_occurred, incident, location, narrative) values (?, ?, ?, ?, ?, ?)", (int(df.iloc[1][0]), df.iloc[1][1], df.iloc[1][2], df.iloc[1][3], df.iloc[1][4], df.iloc[1][5]))

rows = cursor.execute("SELECT * FROM report").fetchall()
print(rows)