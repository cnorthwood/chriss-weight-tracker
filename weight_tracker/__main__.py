#!/usr/bin/env python3

from datetime import date

from weight_tracker.db import last_reading_date, ensure_schema, insert_reading
from weight_tracker.fitbit import weight_readings


def add_readings_to_database():
    if last_reading_date() == date.today():
        return

    for reading in weight_readings(last_reading_date(), date.today()):
        insert_reading(reading)


ensure_schema()
add_readings_to_database()
