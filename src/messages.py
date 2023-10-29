from datetime import datetime, timedelta


def break_up_message_helper(message: str, list: list):
    if len(message) <= 280:
        return list.append(message)

    list.append(message[:277] + "\u2026")
    return break_up_message_helper("\u2026" + message[277:], list)


def break_up_message(message: str):
    messages = []
    break_up_message_helper(message, messages)
    return messages


def create_message_from_report(row):
    date_and_time = row["Date / Time  Occurred *"].split("  ")
    date = date_and_time[0]
    if len(date_and_time) == 1:
        time = row["Time Reported"]
    else:
        time = date_and_time[1]

    message = (
        row["Location"]
        + "\n"
        + date
        + " "
        + time
        + "\n"
        + row["Incident"]
        + "\n"
        + "\n"
        + row["Narrative"]
    )
    message = break_up_message(message)
    return message
