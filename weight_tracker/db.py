from contextlib import closing
from datetime import date, time, datetime
import os
import sqlite3

db = sqlite3.connect(os.environ["FITBIT_DATABASE"])


def ensure_schema():
    with closing(db.cursor()) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                logId INTEGER PRIMARY KEY, 
                readingDate TEXT, 
                weight REAL,
                fat REAL
            )
            """
        )
        db.commit()


def last_reading_date():
    with closing(db.cursor()) as cursor:
        result = cursor.execute("SELECT max(readingDate) FROM readings").fetchone()[0]
        if result is None:
            return None

        return datetime.fromisoformat(result).date()


def insert_reading(reading):
    print(reading)
    with closing(db.cursor()) as cursor:
        cursor.execute(
            "INSERT INTO readings (logId, readingDate, weight, fat) VALUES(?, ?, ?, ?) ON CONFLICT DO NOTHING",
            (
                reading["logId"],
                _reading_datetime(reading).isoformat(),
                reading["weight"],
                reading.get("fat"),
            ),
        )
        db.commit()


def _reading_datetime(reading):
    return datetime.combine(
        date.fromisoformat(reading["date"]), time.fromisoformat(reading["time"])
    )
