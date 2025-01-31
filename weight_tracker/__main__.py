#!/usr/bin/env python3

import argparse
import sys

from weight_tracker.db import ensure_schema


parser = argparse.ArgumentParser()
parser.add_argument("--login", help="run the initial login process", action="store_true")
parser.add_argument("--save-tsv", help="save the results to a TSV file")
parser.add_argument("--google-sheet", help="save the results to a Google Sheet")
args = parser.parse_args()

ensure_schema()
if args.login:
    from weight_tracker.auth import login

    login()
elif args.save_tsv or args.google_sheet:
    from weight_tracker.analysis import day_data, days
    from weight_tracker.fitbit import add_readings_to_database

    add_readings_to_database()
    data = [day_data(day) for day in days()]

    if args.save_tsv:
        from weight_tracker.tsv_file import write_tsv

        write_tsv(args.save_tsv, data)

    if args.google_sheet:
        from weight_tracker.google_sheet import write_google_sheet

        write_google_sheet(args.google_sheet, data)
else:
    parser.print_help()
    sys.exit(1)
