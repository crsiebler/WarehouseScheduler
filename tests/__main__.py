import unittest
import logging
import pandas as pd
import datetime as dt
from pyscheduler.scheduler import Scheduler
from pyscheduler.parser import (
    parse,
    parse_work_hours,
    parse_work_days,
    parse_loading_time,
    parse_departure_time,
    parse_loading_perference,
    parse_line,
)

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)


class TestScheduler(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScheduler, self).__init__(*args, **kwargs)
        self.input1 = "tests/input/input1.txt"
        self.input2 = "tests/input/input2.txt"
        self.input3 = "tests/input/input3.txt"
        self.input4 = "tests/input/input4.txt"
        self.input5 = "tests/input/input5.txt"
        self.input6 = "tests/input/input6.txt"
        self.input7 = "tests/input/input7.txt"

    def test_parse_line(self):
        self.assertEqual(parse_line("A:B"), "B", "Invalid split")
        self.assertEqual(parse_line(" A : B "), "B", "String stripping failed")
        self.assertEqual(parse_line("A:B:C"), "B", "Wrong index on split")

    def test_parse_work_hours(self):
        self.assertTupleEqual(
            parse_work_hours("08:00 ~ 10:00"),
            (dt.time(8, 0), dt.time(10, 0)),
            "Failed parsing time range",
        )
        self.assertTupleEqual(
            parse_work_hours("12:00 ~ 18:00"),
            (dt.time(12, 0), dt.time(18, 0)),
            "Failed parsing 24 hour time range",
        )

    def test_parse_work_days(self):
        self.assertListEqual(
            parse_work_days(
                "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
            ),
            [1, 1, 1, 1, 1, 1, 1],
            "Failed parsing days as CSV",
        )
        self.assertListEqual(
            parse_work_days("Monday, Tuesday, Wednesday, "),
            [1, 1, 1, 0, 0, 0, 0],
            "Failed to account for trailing comma",
        )
        self.assertListEqual(
            parse_work_days("Monday, , Tuesday"),
            [1, 1, 0, 0, 0, 0, 0],
            "Failed to account for empty value given in CSV",
        )
        self.assertListEqual(
            parse_work_days("Monday through Sunday"),
            [1, 1, 1, 1, 1, 1, 1],
            "Failed to parse day range",
        )
        self.assertListEqual(
            parse_work_days("Tuesday, Friday through Sunday"),
            [0, 1, 0, 0, 1, 1, 1],
            "Failed to parse compond range",
        )
        self.assertListEqual(
            parse_work_days("Sunday through Tuesday"),
            [1, 1, 0, 0, 0, 0, 1],
            "Failed to parse range with overlapping start of the week",
        )

    def test_parse_loading_time(self):
        self.assertEqual(parse_loading_time("3 Hours"), pd.Timedelta("0 days 03:00:00"))
        self.assertEqual(
            parse_loading_time("3.5 Hours"), pd.Timedelta("0 days 03:30:00")
        )

    def test_parse_departure_time(self):
        self.assertEqual(
            parse_departure_time("2018-08-13 10:00 (CarvanaLand local timezone)"),
            dt.datetime(2018, 8, 13, 10, 0),
            "Error parsing departure time 1",
        )
        self.assertEqual(
            parse_departure_time("2018-08-15 14:00"),
            dt.datetime(2018, 8, 15, 14, 0),
            "Error parsing departure time 2",
        )
        self.assertEqual(
            parse_departure_time("2018-08-15 10:00"),
            dt.datetime(2018, 8, 15, 10, 0),
            "Error parsing departure time 3",
        )
        self.assertEqual(
            parse_departure_time("2018-08-14 10:00"),
            dt.datetime(2018, 8, 14, 10, 0),
            "Error parsing departure time 4",
        )

    def test_parse_loading_perference(self):
        self.assertEqual(
            parse_loading_perference("Loading time has to be on the same day"),
            Scheduler.SAME_DAY,
            "Failed to parse loading preference for same day",
        )
        self.assertEqual(
            parse_loading_perference(
                "Loading time can be spread across different days"
            ),
            Scheduler.SPREAD,
            "Failed to parse loading preference for can be spread",
        )
        self.assertEqual(
            parse_loading_perference(
                "Loading time cannot be spread across different days"
            ),
            Scheduler.SAME_DAY,
            "Failed to parse loading perference for cannot be spread",
        )

    @unittest.SkipTest
    def test_scheduler(self):
        pass

    @unittest.SkipTest
    def test_input1(self):
        self.assertEqual(parse(self.input1), "2018-08-11 11:00")

    @unittest.SkipTest
    def test_input2(self):
        self.assertEqual(parse(self.input2), "2018-08-13 13:00")

    @unittest.SkipTest
    def test_input3(self):
        self.assertEqual(parse(self.input3), "2018-08-13 13:00")

    @unittest.SkipTest
    def test_input4(self):
        self.assertEqual(parse(self.input4), "2018-08-13 13:00")

    @unittest.SkipTest
    def test_input5(self):
        self.assertEqual(parse(self.input5), "2018-08-13 13:00")

    @unittest.SkipTest
    def test_input6(self):
        self.assertEqual(parse(self.input6), "2018-08-13 13:00")

    @unittest.SkipTest
    def test_input7(self):
        self.assertEqual(parse(self.input7), "2018-08-13 13:00")


if __name__ == "__main__":
    unittest.main()
