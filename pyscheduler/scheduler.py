import datetime as dt
import pandas as pd
import timeboard as tb
from typing import List, Tuple, Union, Optional
from enum import Enum

from timeboard import workshift

Shift = Tuple[dt.time, dt.time]
OperatingHours = List[int]


class Weekday(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


def seconds_to_minutes(seconds: int, round: Optional[bool] = True) -> Union[int, float]:
    """"""
    return int(seconds / 60) if round else seconds / 60


class InvalidScheduleException(Exception):
    """"""

    def __init__(self, shift_duration: int, loading_time: dt.timedelta):
        self.shift_duration = shift_duration
        self.loading_time = loading_time

    def __str__(self) -> str:
        return f"Shift duration ({seconds_to_minutes(self.shift_duration)} minutes) less than loading time ({seconds_to_minutes(self.loading_time.total_seconds())} minutes)"


class Scheduler:
    """"""

    SAME_DAY = 0
    SPREAD = 1
    DELTA = pd.to_timedelta("8 days")

    def __init__(
        self,
        shift: Shift,
        working_days: OperatingHours,
        loading_time: dt.timedelta,
        loading_preference: int,
        departure_time: dt.datetime,
    ):
        start_time = {"hour": shift[0].hour, "minute": shift[0].minute}
        end_time = {"hour": shift[1].hour, "minute": shift[1].minute}

        day_parts = tb.Marker(each="D", at=[start_time, end_time])
        day = tb.Organizer(marker=day_parts, structure=[0, 1, 0])

        day_structure = [day if working else 0 for working in working_days]
        weekly = tb.Organizer(marker="D", structure=day_structure)

        self.timeboard = tb.Timeboard(
            base_unit_freq="S",
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

    @staticmethod
    def cmp_wrkshf_dur(workshift: tb.Workshift, delta: dt.timedelta) -> int:
        return workshift.duration - delta.total_seconds()

    def _departure_on_duty(self) -> bool:
        """"""
        return self.timeboard(self.departure_time).is_on_duty()

    def _deadline_spread(self) -> pd.Timestamp:
        """"""
        return ""

    def _deadline_same_day(self) -> pd.Timestamp:
        """"""
        # Get the workshift on the deadline
        workshift = self.timeboard(self.departure_time)

        # Departure was on duty, see if there is enough time to meet deadline
        if (
            self._departure_on_duty()
            and self.cmp_wrkshf_dur(workshift, self.loading_time) > 0
        ):
            # There is enough time to schedule the loading on same workshift
            return self.departure_time - self.loading_time
        elif self.cmp_wrkshf_dur(workshift.rollback(1), self.loading_time) > 0:
            # Not enough time to schedule loading same day so get previous on duty workshift
            return workshift.rollback(1).end_time - self.loading_time
        else:
            # Departure was not on duty so get closest workshift
            raise InvalidScheduleException(workshift.duration, self.loading_time)

    def deadline(self) -> pd.Timestamp:
        """"""
        # Two different strategies will need to be used to find deadline
        if self.loading_preference:
            # The loading time can be spread out of multiple shifts
            return self._deadline_spread()
        else:
            # The loading time must be completed all on the same day
            print(f"{self.timeboard}")
            return self._deadline_same_day()