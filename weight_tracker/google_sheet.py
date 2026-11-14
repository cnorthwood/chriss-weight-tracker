import google.auth
import gspread
from gspread.utils import ValueInputOption


def write_google_sheet(sheet_url, data):
    # Application Default Credentials: a service account key, or a workload identity federation config, named by
    # GOOGLE_APPLICATION_CREDENTIALS
    credentials, _ = google.auth.default(scopes=gspread.auth.DEFAULT_SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(sheet_url).get_worksheet(0)

    sheet.update(
        [
            [
                d["date"],
                d["weight"],
                d["bmi"],
                "",
                d["moving_average_weight"],
                d["moving_average_bmi"],
                "",
                d["weekly_weight_delta"],
                d["weekly_bmi_delta"],
                "",
                d["monthly_weight_delta"],
                d["monthly_bmi_delta"],
            ]
            for d in data
        ],
        f"A3:L{3+len(data)}",
        value_input_option=ValueInputOption.user_entered,
    )
