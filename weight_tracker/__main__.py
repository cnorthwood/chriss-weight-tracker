#!/usr/bin/env python3

from datetime import date

from weight_tracker.fitbit import weight_info

print(weight_info(date(2024, 1, 1), date(2024, 1, 10)))
