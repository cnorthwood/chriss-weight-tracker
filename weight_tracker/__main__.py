#!/usr/bin/env python3

from datetime import date
import sys

from weight_tracker.analysis import day_data, days
from weight_tracker.db import last_reading_date, ensure_schema, insert_reading
from weight_tracker.fitbit import weight_readings


def add_readings_to_database():
    if last_reading_date() == date.today():
        return

    for reading in weight_readings(last_reading_date(), date.today()):
        insert_reading(reading)


def write_tsv(filename, data):
    with open(filename, "w") as output_tsv:
        for d in data:
            fields = [
                d["date"],
                d["weight"],
                d["bmi"],
                d["fat_percentage"],
                d["fat_weight"],
                "",
                d["moving_average_weight"],
                d["moving_average_bmi"],
                d["moving_average_fat_percentage"],
                d["moving_average_fat_weight"],
                "",
                d["weekly_weight_delta"],
                d["weekly_bmi_delta"],
                d["weekly_fat_percentage_delta"],
                d["weekly_fat_weight_delta"],
                "",
                d["monthly_weight_delta"],
                d["monthly_bmi_delta"],
                d["monthly_fat_percentage_delta"],
                d["monthly_fat_weight_delta"],
            ]
            output_tsv.write("\t".join(fields) + "\n")


ensure_schema()
add_readings_to_database()
write_tsv(sys.argv[1], (day_data(day) for day in days()))
