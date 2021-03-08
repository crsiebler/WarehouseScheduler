import logging
import datetime as dt
import pandas as pd
import timeboard as tb
from enum import Enum
from typing import List, Tuple, Union, Optional
from dateutil.relativedelta import relativedelta, MO


Shift = Tuple[dt.time, dt.time]
WorkingDays = List[int]


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def seconds_to_minutes(seconds: int, round: Optional[bool] = True) -> Union[int, float]:
    """Convert seconds to minutes."""
    return int(seconds / 60) if round else seconds / 60


class InvalidScheduleException(Exception):
    """Exception got when a schedule cannot meet the parameters requested."""

    def __init__(self, shift_duration: int, loading_time: dt.timedelta):
        self.shift_duration = shift_duration
        self.loading_time = loading_time

    def __str__(self) -> str:
        return (
            f"Shift duration ({seconds_to_minutes(self.shift_duration)} "
            f"minutes) less than loading time "
            f"({seconds_to_minutes(self.loading_time.total_seconds())} minutes)"
        )


class Scheduler:
    """Take in a user defined schedule and produce a deadline for an order.

    The bulk of the work is accomplished by the timeboard object (Thank you to
    https://github.com/mmamaev for creating an awesome library to utilize for
    this project). Using a timeboard greatly lowered the complexity for knowing
    what days are on duty and getting the previous working day(s).
    """

    SAME_DAY = 0
    SPREAD = 1

    def __init__(
        self,
        shift: Shift,
        working_days: WorkingDays,
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

        # The timeboard must start on a Monday for the day structure form
        timeboard_start = departure_time + relativedelta(weekday=MO(-2))

        self.timeboard = tb.Timeboard(
            base_unit_freq="S",
            start=timeboard_start,
            end=departure_time,
            layout=weekly,
        )
        self.departure_time = departure_time
        self.loading_time = loading_time
        self.loading_preference = loading_preference

        logging.info(f"Shift: {shift})")
        logging.info(f"Working Days: {working_days}")
        logging.info(f"Timeboard: {self.timeboard}")

    def __repr__(self) -> str:
        return f"Scheduler(TimeBoard,Departure,LoadingTime,LoadingPreference)"

    def __str__(self) -> str:
        return (
            f"Timeboard: {self.timeboard}\n"
            f"Departure: {self.departure_time}\n"
            f"Loading Time: {self.loading_time}\n"
            f"Loading Preference: "
            f"{'Spread' if self.loading_preference else 'Same Day'}\n"
        )

    @staticmethod
    def compare_shift(workshift: tb.Workshift, delta: int) -> int:
        """Difference in the workshift duration and a delta in seconds.

        The warehouse loading time is generally used for the timedelta, but any
        timedelta could be used to compare the workshift duration. The duration
        of the workshift is based on the frequency specified when the timeboard
        is created. For this example it is in seconds.
        """
        return workshift.duration - delta

    def _lt_sec(self) -> int:
        """Retreive the loading time in seconds."""
        return self.loading_time.total_seconds()

    def _get_departure_shift(self) -> tb.Workshift:
        """Retreive the workshift for the requested departure time.

        Subtract a microsecond to accommodate for departure times that fall on
        the exact time a shift ends.
        """
        return self.timeboard(self.departure_time - dt.timedelta(microseconds=1))

    def _departure_on_duty(self) -> bool:
        """Figure out if the shift the departure falls on is on duty"""
        return self._get_departure_shift().is_on_duty()

    def _deadline_spread(self) -> pd.Timestamp:
        """Find the deadline for a departure time with loading spread out."""
        shift_idx = 0
        remaining_work = self._lt_sec()
        workshift = self._get_departure_shift()
        # Continue working on order until no remaining work to meet deadline
        while self.compare_shift(workshift.rollback(shift_idx), remaining_work) <= 0:
            remaining_work -= workshift.duration
            logging.info(f"Shift: {shift_idx}, Remaining: {remaining_work}")
            shift_idx += 1

        return workshift.rollback(shift_idx).end_time - dt.timedelta(
            seconds=remaining_work
        )

    def _deadline_same_day(self) -> pd.Timestamp:
        """Find the deadline for a departure time with a same day loading time.

        Raises:
            InvalidScheduleException: Because the loading time cannot be
                segmented, there is a possibility the working shifts do not
                contained enough time to fulfill the order.
        """
        # Get the workshift on the deadline
        workshift = self._get_departure_shift()

        # Departure was on duty, see if there is enough time to meet deadline
        if (
            self._departure_on_duty()
            and self.compare_shift(workshift, self._lt_sec()) > 0
        ):
            # There is enough time to schedule the loading on same workshift
            return workshift.end_time - self.loading_time
        elif self.compare_shift(workshift.rollback(1), self._lt_sec()) > 0:
            # Not enough time to schedule loading same day so get previous on duty workshift
            return workshift.rollback(1).end_time - self.loading_time
        else:
            # Departure was not on duty so get closest workshift
            raise InvalidScheduleException(workshift.duration, self.loading_time)

    def deadline(self) -> pd.Timestamp:
        """Find the deadline for a warehouse work to fulfill an order.

        Two different strategies will need to be used to find deadline
        """
        if self.loading_preference:
            # The loading time can be spread out of multiple shifts
            logging.info(f"Calculating: Spread Order Deadline")
            return self._deadline_spread()
        else:
            # The loading time must be completed all on the same day
            logging.info(f"Calculating: Same Day Order Deadline")
            return self._deadline_same_day()