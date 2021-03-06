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
    DELTA = pd.to_timedelta("7 days")

    def __init__(
        self, shift, working_days, loading_time, loading_preference, departure_time
    ):
        self.departure_time = departure_time
        self.loading_time = loading_time
        self.loading_preference = loading_preference
        start_time = {"hour": shift[0].hour, "minute": shift[0].minute}
        end_time = {"hour": shift[1].hour, "minute": shift[1].minute}
        day_parts = tb.Marker(each="D", at=[start_time, end_time])
        hours_of_operation = tb.Organizer(marker=day_parts, structure=[1, 0])
        days_of_operation = tb.Organizer(marker="W", structure=[working_days])
        self.timeboard = tb.Timeboard(
            base_unit_freq="D",
            start=departure_time - self.DELTA,
            end=departure_time,
            layout=days_of_operation,
            default_name="day_of_operation",
            worktime_source="labels",
        )

        # winter = tb.Organizer(marker="W", structure=[[0, 0, 6, 6, 0, 0, 0]])
        # summer = tb.Organizer(marker="W", structure=[[0, 8, 8, 8, 8, 10, 10]])
        # seasons = tb.Marker(
        #     each="A",
        #     at=[
        #         {"month": 5, "weekday": 1, "week": 1, "shift": 1},
        #         {"month": 9, "weekday": 7, "week": -1},
        #     ],
        #     how="nth_weekday_of_month",
        # )
        # seasonal = tb.Organizer(marker=seasons, structure=[winter, summer])
        # self.timeboard = tb.Timeboard(
        #     base_unit_freq="D",
        #     start="01 Jan 2012",
        #     end="31 Dec 2015",
        #     layout=seasonal,
        #     worktime_source="labels",
        # )

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""

    def start() -> str:
        return ""