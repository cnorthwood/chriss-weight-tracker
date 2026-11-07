from datetime import datetime
import os
import sqlite3

db = sqlite3.connect(os.environ["WEIGHT_DATABASE"])
cursor = db.cursor()


def ensure_schema():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS readings (
            logId INTEGER PRIMARY KEY,
            readingDate TEXT,
            weight REAL
        )
        """
    )
    # Google Health's IDs for readings don't match the Fitbit logIds already stored, so readings are identified
    # by when they were taken instead
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS readings_reading_date ON readings (readingDate)")
    db.commit()


def last_reading_date():
    result = cursor.execute("SELECT max(readingDate) FROM readings").fetchone()[0]
    if result is None:
        return None

    return datetime.fromisoformat(result).date()


def first_reading_date():
    result = cursor.execute("SELECT min(readingDate) FROM readings").fetchone()[0]
    return datetime.fromisoformat(result).date()


def insert_reading(reading_time: datetime, weight_kg: float):
    cursor.execute(
        "INSERT INTO readings (readingDate, weight) VALUES(?, ?) ON CONFLICT DO NOTHING",
        (reading_time.isoformat(), weight_kg),
    )
    db.commit()


def get_weight_in_range(start_time, end_time):
    results = cursor.execute(
        "SELECT weight FROM readings WHERE readingDate >= ? AND readingDate <= ? AND weight IS NOT NULL",
        (start_time.isoformat(), end_time.isoformat()),
    ).fetchall()
    return [result[0] for result in results]


def get_last_known_weight_at(point_in_time):
    result = cursor.execute(
        "SELECT weight FROM readings WHERE readingDate <= ? ORDER BY readingDate DESC LIMIT 1",
        (point_in_time.isoformat(),),
    ).fetchone()
    if result is None:
        result = cursor.execute(
            "SELECT weight FROM readings ORDER BY readingDate ASC LIMIT 1"
        ).fetchone()

    return result[0]
