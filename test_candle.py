from unittest import TestCase
from Candle import Candle
import datetime


class TestCandle(TestCase):
    def test_convert_str_to_date(self):
        empty = datetime.date(2001, 1, 1)
        self.assertEqual(datetime.date(2017, 10, 30), Candle.convert_str_to_date("30102017"), "normal date")
        self.assertEqual(empty, Candle.convert_str_to_date("efaffef"), "letters in input")
        self.assertEqual(empty, Candle.convert_str_to_date("20171030"), "reverse format")
        self.assertEqual(empty, Candle.convert_str_to_date("20170230"), "invalid date")
        self.assertEqual(empty, Candle.convert_str_to_date("201723"), "too short date")
        self.assertEqual(empty, Candle.convert_str_to_date("20170230"), "too long date")

    def test_convert_str_to_time(self):
        time = datetime.time(0, 0, 0)
        self.assertEqual(datetime.time(10, 15, 55), Candle.convert_str_to_time("101555"), "normal time")
        self.assertEqual(time, Candle.convert_str_to_time("101566"), "wrong time")
        self.assertEqual(time, Candle.convert_str_to_time("1015666"), "too long time")
        self.assertEqual(time, Candle.convert_str_to_time("1015"), "too short time")
        self.assertEqual(time, Candle.convert_str_to_time("AABBCC"), "letters time")

    def test_to_string(self):
        candle = Candle.from_string("01042017;100001;150.12345;151.54321;149.123456;151.9874651;79844")
        self.assertEqual(candle.to_string(),
                         "01042017;100001;150.1234;151.5432;149.1235;151.9875;79844", "string conversion's format")

    def test_from_string(self):
        candle = Candle.from_string("01042017;100001;150;151.5;149;121;79844")
        self.assertEqual(candle.filled, True, "normal string")
        self.assertEqual(candle.close, 121)
        candle = Candle.from_string("010420171;100001;150;151.5;149;121;79844")
        self.assertEqual(candle.filled, False, "invalid date")
        candle = Candle.from_string("01042017;100001;150;151.5;abc;121;79844")
        self.assertEqual(candle.filled, False, "invalid float value")
        candle = Candle.from_string("01042017;100001;150;151.5;149;121;79844;45")
        self.assertEqual(candle.filled, False, "too much data")
        candle = Candle.from_string("01042017;150;151.5;149;121;79844")
        self.assertEqual(candle.filled, False, "no time")

    def test_from_candle(self):
        source = Candle()
        source.date = "30092017"
        source.time = "154523"
        source.init_datetime()

        candle = Candle.from_candle(source)
        self.assertTrue(candle.filled, "candle not filled")
        self.assertTrue(candle.is_same_time(source), "date&time copying")

    def test_make_spread(self):
        candle2 = Candle.from_string("01042017;100001;100;100;100;100;123")
        candle1 = Candle.from_string("01042017;100001;200;200;200;200;123")

        spread = Candle.make_spread(candle1, 1, candle2, 1)
        self.assertEqual(spread.close, 100, "subtraction without coefficients")
        spread = Candle.make_spread(candle1, 1.5, candle2, 0.8)
        self.assertEqual(spread.close, 220, "subtraction with coefficients")

    def test_is_older(self):
        candle1 = Candle.from_string("01042017;100001;200;200;200;200;123")
        candle2 = Candle.from_string("01042017;120001;100;100;100;100;123")
        self.assertTrue(candle1.is_older(candle2), "older, 2 hours")

        candle2 = Candle.from_string("30042017;100001;100;100;100;100;123")
        self.assertTrue(candle1.is_older(candle2), "older, 29 days")

        candle2 = Candle.from_string("30032017;100001;100;100;100;100;123")
        self.assertFalse(candle1.is_older(candle2), "younger")

    def test_is_same_time(self):
        candle1 = Candle.from_string("01042017;100001;200;200;200;200;123")
        candle2 = Candle.from_string("01042017;100001;100;100;100;100;123")
        self.assertTrue( candle1.is_same_time(candle2), "equal dates")

        candle2 = Candle.from_string("01042017;100002;100;100;100;100;123")
        self.assertFalse(candle1.is_same_time(candle2), "not equal dates")

