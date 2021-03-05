import unittest
from pyscheduler.parser import parse


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

    def test_input1(self):
        self.assertEqual(parse(self.input1), '2018-08-11 11:00')

    def test_input2(self):
        self.assertEqual(parse(self.input2), '2018-08-13 13:00')

    def test_input3(self):
        self.assertEqual(parse(self.input3), '2018-08-13 13:00')

    def test_input4(self):
        self.assertEqual(parse(self.input4), '2018-08-13 13:00')

    def test_input5(self):
        self.assertEqual(parse(self.input5), '2018-08-13 13:00')

    def test_input6(self):
        self.assertEqual(parse(self.input6), '2018-08-13 13:00')

    def test_input7(self):
        self.assertEqual(parse(self.input7), '2018-08-13 13:00')


if __name__ == "__main__":
    unittest.main()
