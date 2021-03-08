import logging
import pandas as pd
import datetime as dt
from typing import Tuple, TextIO, List
from .scheduler import InvalidScheduleException, Weekday, Scheduler

Layout = List[int]
Shift = Tuple[dt.time, dt.time]


def parse_work_hours(raw: str) -> Shift:
    """"""
    SEPARATOR = "~"

    def parse_hour(raw: str):
        """"""
        return pd.to_datetime(raw.strip(), format="%H:%M").time()

    return tuple([parse_hour(split) for split in raw.split(SEPARATOR)])


def parse_work_days(raw: str) -> Layout:
    """"""
    SEPARATOR = ","
    RANGE = "through"
    layout = [0] * 7

    def set_weekday(value: int) -> None:
        """"""
        layout[value] = 1

    def parse_weekday(raw: str) -> int:
        """"""
        return Weekday[raw.strip().upper()].value

    def parse_range(raw: str) -> Layout:
        """"""
        start, end = tuple([parse_weekday(split) for split in raw.split(RANGE)])
        if start > end:
            [set_weekday(x % 7) for x in range(start, end + 8)]
        else:
            [set_weekday(x) for x in range(start, end + 1)]
        return layout

    def parse_csv(raw: str) -> Layout:
        """"""
        for day in raw.split(SEPARATOR):
            # Check for a range given in a CSV
            if RANGE in day:
                parse_range(day)
            # Check for an empty value given in CSV
            elif not day.strip():
                logging.warning("Empty value given in working days")
            else:
                set_weekday(parse_weekday(day))
        return layout

    return parse_csv(raw) if SEPARATOR in raw else parse_range(raw)


def parse_loading_time(raw: str):
    """"""
    return pd.to_timedelta(raw.strip())


def parse_departure_time(raw: str):
    """"""
    return pd.to_datetime(raw.split("(")[0].strip(), format="%Y-%m-%d %H:%M")


def parse_loading_perference(raw: str):
    """"""
    KEYWORD_SAME_DAY = "same day"
    KEYWORD_CANNOT = "cannot"
    return (
        Scheduler.SAME_DAY
        if KEYWORD_SAME_DAY in raw or KEYWORD_CANNOT in raw
        else Scheduler.SPREAD
    )


def parse_line(line: str) -> str:
    """"""
    return ":".join(line.split(":")[1:])


def parse_schedule(input: TextIO):
    """"""
    raw_work_hours = parse_line(input.readline())
    raw_work_days = parse_line(input.readline())
    raw_loading_time = parse_line(input.readline())
    raw_departure_time = parse_line(input.readline())
    raw_loading_perference = input.readline()

    return {
        "shift": parse_work_hours(raw_work_hours),
        "working_days": parse_work_days(raw_work_days),
        "loading_time": parse_loading_time(raw_loading_time),
        "loading_preference": parse_loading_perference(raw_loading_perference),
        "departure_time": parse_departure_time(raw_departure_time),
    }


def parse(input_file: str) -> None:
    """"""
    # Read the input file to determine the warehouse schedule
    with open(input_file, "r") as input:
        result = "Unknown"
        try:
            scheduler = Scheduler(**parse_schedule(input))
            result = scheduler.deadline()
            print(f"{result.round('T')}")
        except InvalidScheduleException as ise:
            logging.error(ise)

        return result