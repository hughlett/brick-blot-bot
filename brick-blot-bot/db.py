import sqlite3
from contextlib import closing
from pandas import DataFrame


def create_table() -> None:
    """_summary_"""
    with closing(sqlite3.connect("reports.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "CREATE TABLE report (report_number INTEGER, time_reported TEXT, date_time_occurred TEXT, incident TEXT, location TEXT, narrative TEXT)"
            )


def insert_row(
    report_number: int,
    time_reported: str,
    date_time_occurred: str,
    incident: str,
    location: str,
    narrative: str,
) -> None:
    """_summary_

    Args:
        report_number (int): _description_
        time_reported (str): _description_
        date_time_occurred (str): _description_
        incident (str): _description_
        location (str): _description_
        narrative (str): _description_
    """
    with closing(sqlite3.connect("reports.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO report (report_number, time_reported, date_time_occurred, incident, location, narrative) values (?, ?, ?, ?, ?, ?)",
                (
                    report_number,
                    time_reported,
                    date_time_occurred,
                    incident,
                    location,
                    narrative,
                ),
            )
        connection.commit()


def insert_report(report: DataFrame) -> None:
    """_summary_

    Args:
        report (DataFrame): _description_
    """
    insert_row(
        report["Report Number"],
        report["Time Reported"],
        report["Date / Time  Occurred *"],
        report["Incident"],
        report["Location"],
        report["Narrative"],
    )


def report_exists(report_number: int) -> bool:
    """_summary_

    Args:
        report_number (int): _description_

    Returns:
        bool: _description_
    """
    with closing(sqlite3.connect("reports.db")) as connection:
        with closing(connection.cursor()) as cursor:
            match = cursor.execute(
                "SELECT report_number from report WHERE report_number = ?",
                (report_number,),
            ).fetchone()
            return True if match else False
