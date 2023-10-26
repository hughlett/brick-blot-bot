from datetime import datetime, timedelta


def break_up_message_helper(message: str, list: list):
    if len(message) <= 280:
        return list.append(message)    
    return break_up_message_helper('\u2026' + message[277:], list.append(message[:277] + '\u2026'))


def break_up_message(message: str):
    messages = []
    break_up_message_helper(message, messages)
    return messages


def create_message_from_report(row):
    if row['Date / Time Occurred *'] == 'nan':
        date = (datetime.today() - timedelta(1)).strftime('%-m/%-d/%y')
        time = row['Time Reported'].replace(' ', '')
    elif ' - ' in row['Date / Time Occurred *']:
        date = row['Date / Time Occurred *']
        time = 'Unknown time'
    else:
        date_and_time = row['Date / Time Occurred *'].split("  ")
        date = date_and_time[0]
        if len(date_and_time) == 1:
            time = 'Unknown time'
        else:
            time = date_and_time[1]

        if 'Unknown' in date:
            date = 'Unknown date'

        if 'Unknown' in time:
            time = 'Unknown time'

    message = row['Location'] + '\n' + date + ' ' + time + \
        '\n' + row['Incident'] + '\n' + '\n' + row['Narrative']
    message = break_up_message(message)
    return message
