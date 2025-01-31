import os

import gspread
from gspread.utils import ValueInputOption


def write_google_sheet(sheet_url, data):
    client = gspread.service_account(os.environ["GOOGLE_SERVICE_ACCOUNT"])
    sheet = client.open_by_url(sheet_url).get_worksheet(0)

    sheet.update(
        [
            [
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
            for d in data
        ],
        f"A3:T{3+len(data)}",
        value_input_option=ValueInputOption.user_entered,
    )
