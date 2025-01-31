#!/usr/bin/env python3

import argparse
import sys

from weight_tracker.db import ensure_schema


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


parser = argparse.ArgumentParser()
modes = parser.add_mutually_exclusive_group()
modes.add_argument("--login", help="run the initial login process", action="store_true")
modes.add_argument("--save-tsv", help="save the results to a TSV file")
args = parser.parse_args()

ensure_schema()
if args.login:
    from weight_tracker.auth import login

    login()
elif args.save_tsv:
    from weight_tracker.analysis import day_data, days
    from weight_tracker.fitbit import add_readings_to_database

    add_readings_to_database()
    write_tsv(args.save_tsv, (day_data(day) for day in days()))
else:
    parser.print_help()
