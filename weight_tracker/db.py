from datetime import datetime, date, time
import json
import os
import sqlite3

db = sqlite3.connect(os.environ["FITBIT_DATABASE"])
cursor = db.cursor()


def ensure_schema():
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
    result = cursor.execute("SELECT max(readingDate) FROM readings").fetchone()[0]
    if result is None:
        return None

    return datetime.fromisoformat(result).date()


def first_reading_date():
    result = cursor.execute("SELECT min(readingDate) FROM readings").fetchone()[0]
    return datetime.fromisoformat(result).date()


def insert_reading(reading):
    cursor.execute(
        "INSERT INTO readings (logId, readingDate, weight, fat) VALUES(?, ?, ?, ?) ON CONFLICT DO NOTHING",
        (
            reading["logId"],
            reading_datetime(reading).isoformat(),
            reading["weight"],
            reading.get("fat"),
        ),
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


def get_fat_in_range(start_time, end_time):
    results = cursor.execute(
        "SELECT fat FROM readings WHERE readingDate >= ? AND readingDate <= ? AND fat IS NOT NULL",
        (start_time.isoformat(), end_time.isoformat()),
    ).fetchall()
    return [result[0] for result in results]


def get_last_known_fat_at(point_in_time):
    result = cursor.execute(
        "SELECT fat FROM readings WHERE readingDate <= ? AND fat IS NOT NULL ORDER BY readingDate DESC LIMIT 1",
        (point_in_time.isoformat(),),
    ).fetchone()
    if result is None:
        result = cursor.execute(
            "SELECT fat FROM readings WHERE fat IS NOT NULL ORDER BY readingDate ASC LIMIT 1"
        ).fetchone()

    return result[0]


def reading_datetime(reading):
    return datetime.combine(
        date.fromisoformat(reading["date"]), time.fromisoformat(reading["time"])
    )
