import sqlite3
from contextlib import closing


def create_table() -> None:
    with closing(sqlite3.connect("reports.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "CREATE TABLE report (report_number INTEGER, time_reported TEXT, date_time_occurred TEXT, incident TEXT, location TEXT, narrative TEXT)"
            )


def insert_row(
    report_number, time_reported, date_time_occurred, incident, location, narrative
) -> None:
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


def insert_report(report) -> None:
    insert_row(
        report["Report Number"],
        report["Time Reported"],
        report["Date / Time  Occurred *"],
        report["Incident"],
        report["Location"],
        report["Narrative"],
    )


def report_exists(report_number) -> bool:
    with closing(sqlite3.connect("reports.db")) as connection:
        with closing(connection.cursor()) as cursor:
            match = cursor.execute(
                "SELECT report_number from report WHERE report_number = ?",
                (report_number,),
            ).fetchone()
            return True if match else False
