import pandas as pd
import timeboard as tb
from enum import Enum


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Scheduler:
    """"""

    SAME_DAY = 0
    SPREAD = 1
    DELTA = pd.to_timedelta("8 days")

    def __init__(
        self, shift, working_days, loading_time, loading_preference, departure_time
    ):
        start_time = {"hour": shift[0].hour, "minute": shift[0].minute}
        end_time = {"hour": shift[1].hour, "minute": shift[1].minute}

        day_parts = tb.Marker(each="D", at=[start_time, end_time])
        day = tb.Organizer(marker=day_parts, structure=[0, 1, 0])

        day_structure = [day if working else 0 for working in working_days]
        weekly = tb.Organizer(marker="D", structure=day_structure)

        self.timeboard = tb.Timeboard(
            base_unit_freq="T",
            start=departure_time - self.DELTA,
            end=departure_time,
            layout=weekly,
        )
        self.departure_time = departure_time
        self.loading_time = loading_time
        self.loading_preference = loading_preference

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""

    def start() -> str:
        return ""