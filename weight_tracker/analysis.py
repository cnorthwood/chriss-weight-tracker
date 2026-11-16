import os
from datetime import timedelta, time, datetime
from statistics import mean

from weight_tracker.db import (
    last_reading_date,
    first_reading_date,
    get_weight_in_range,
    get_last_known_weight_at,
)


def days():
    day = first_reading_date()
    while day <= last_reading_date():
        yield day
        day += timedelta(days=1)


def day_data(day):
    last_week = day - timedelta(days=7)
    last_month = day - timedelta(days=30)

    todays_weight = weight_for(day)
    moving_average_weight = moving_average_weight_for(day)
    last_weeks_moving_average_weight = moving_average_weight_for(last_week)
    last_months_moving_average_weight = moving_average_weight_for(last_month)

    return {
        "date": day.strftime("%d/%m/%Y"),
        "weight": f"{todays_weight:.1f}",
        "bmi": f"{bmi(todays_weight):.2f}",
        "moving_average_weight": f"{moving_average_weight:.1f}",
        "moving_average_bmi": f"{bmi(moving_average_weight):.2f}",
        "weekly_weight_delta": f"{moving_average_weight - last_weeks_moving_average_weight:.1f}",
        "weekly_bmi_delta": f"{bmi(moving_average_weight) - bmi(last_weeks_moving_average_weight):.2f}",
        "monthly_weight_delta": f"{moving_average_weight - last_months_moving_average_weight:.1f}",
        "monthly_bmi_delta": f"{bmi(moving_average_weight) - bmi(last_months_moving_average_weight):.2f}",
    }


MOVING_AVERAGE_DAYS = 7


def moving_average_weight_for(end_day):
    # Both ends of the range are inclusive, so the window starts (N - 1) days before the end day
    start_day = end_day - timedelta(days=MOVING_AVERAGE_DAYS - 1)
    return weight_for(start_day, end_day)


def weight_for(start_day, end_day=None):
    return _mean_reading_for(
        get_weight_in_range, get_last_known_weight_at, start_day, end_day
    )


def _mean_reading_for(reading_f, fallback_f, start_day, end_day=None):
    if end_day is None:
        end_day = start_day
    start_time = datetime.combine(start_day, time.min)
    end_time = datetime.combine(end_day, time.max)
    readings = reading_f(start_time, end_time)
    if len(readings) == 0:
        return fallback_f(start_time)

    return mean(readings)


def bmi(weight):
    height = int(os.environ["HEIGHT"]) / 100
    return weight / height**2
