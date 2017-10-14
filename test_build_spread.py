from unittest import TestCase
import builder


class TestBuild_spread(TestCase):
    def test_build_spread_intersection(self):
        lst1 = ["01012017;100001;0;0;0;0;0",
                "01012017;100002;0;0;0;0;0",
                "01012017;100003;0;0;0;0;0"]
        lst2 = ["01012017;100001;0;0;0;0;0",
                "01012017;100002;0;0;0;0;0",
                "01012017;100003;0;0;0;0;0",
                "01012017;100004;0;0;0;0;0"]
        spread = builder.build_spread(lst1, lst2, 1, 1)

        self.assertEqual(len(spread), len(lst1))

    def test_build_spread_first_older(self):
        lst1 = ["01012016;100001;0;0;0;0;0",
                "01012016;100002;0;0;0;0;0",
                "01012017;090003;0;0;0;0;0",
                "01012017;090004;0;0;0;0;0"]
        lst2 = ["01012017;100001;0;0;0;0;0",
                "01012017;100002;0;0;0;0;0",
                "01012017;100003;0;0;0;0;0"]
        spread = builder.build_spread(lst1, lst2, 1, 1)

        self.assertEqual(len(spread), 0)

    def test_build_spread_second_older(self):
        lst1 = ["01012017;100001;0;0;0;0;0",
                "01012017;100002;0;0;0;0;0",
                "01012017;100003;0;0;0;0;0",
                "01012017;100004;0;0;0;0;0"]
        lst2 = ["01012017;100001;0;0;0;0;0",
                "02012017;100002;0;0;0;0;0",
                "02012017;100003;0;0;0;0;0",
                "05012017;100004;0;0;0;0;0"]
        spread = builder.build_spread(lst1, lst2, 1, 1)

        self.assertEqual(len(spread), 1)
