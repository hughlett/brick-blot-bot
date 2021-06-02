from datetime import datetime, timedelta

def break_up_message_helper(message: str, list: list):
    if len(message) <= 280:
        list.append(message)
        return
    start_of_message = message[:277] + '\u2026'
    list.append(start_of_message)
    end_of_message = '\u2026' + message[277:]
    return break_up_message_helper(end_of_message, list)

def break_up_message(message: str):
    messages = []
    break_up_message_helper(message, messages)
    return messages

def create_message_from_report(row):
    date_and_time = row['Date / Time Occurred *'].replace("  ", " ")
    if date_and_time == 'nan':
        date = (datetime.today() - timedelta(1)).strftime('%-m/%-d/%y')
        date_and_time = date + ' ' + row['Time Reported'].replace(' ', '')
    message = row['Location'] + '\n' + date_and_time + '\n' + row['Incident'] + '\n' + '\n' + row['Narrative']
    
    if 'Unknown' in date_and_time:
        message = 'Unknown location and time' + '\n' + row['Incident'] + '\n' + '\n' + row['Narrative']
    message = break_up_message(message)
    return message

def get_reports_as_messages(df):
    reports = []
    for index, row in df.iterrows():
        report = create_message_from_report(row)
        reports.append(report)
    return reports