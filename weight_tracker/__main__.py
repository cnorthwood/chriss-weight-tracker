#!/usr/bin/env python3

import argparse
import sys

from weight_tracker.db import ensure_schema


def run_as_cli(tsv_file, google_sheet_url):
    from weight_tracker.auth import start_login, complete_login
    from weight_tracker.analysis import day_data, days
    from weight_tracker.fitbit import add_readings_to_database

    oauth_session, auth_url = start_login()
    print(f"Now visit {auth_url} and copy the URL you are redirected to")
    response_url = input("Paste the redirect URL here: ")
    complete_login(oauth_session, response_url)

    add_readings_to_database(oauth_session)
    data = [day_data(day) for day in days()]

    if tsv_file:
        from weight_tracker.tsv_file import write_tsv

        write_tsv(tsv_file, data)

    if google_sheet_url:
        from weight_tracker.google_sheet import write_google_sheet

        write_google_sheet(google_sheet_url, data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="start a webserver serving on the specified port which when accessed takes you through the auth process and syncs the results to a Google Sheet")
    parser.add_argument("--save-tsv", help="run as a CLI tool and save the results to a TSV file")
    parser.add_argument("--google-sheet", help="run as a CLI tool and save the results to a Google Sheet")
    args = parser.parse_args()

    ensure_schema()

    if args.save_tsv or args.google_sheet:
        if args.server:
            pass
        else:
            run_as_cli(args.save_tsv, args.google_sheet)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()