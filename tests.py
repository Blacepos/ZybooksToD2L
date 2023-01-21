import unittest
from zybooks_to_d2l import *
from assumptions import *

class Tests(unittest.TestCase):
    def test_zybooks_row_getter(self):
        # Check that it at least works
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "austi121@msu.edu", "160355379", "2023-01-20 11:59 PM EST", "100")
        getter = ZybooksRowGetter(row)

        self.assertEqual("austi121", getter.netid)
        self.assertEqual("10.00", getter.points_grade)
        self.assertEqual("#", getter.end_of_line_indicator)

        # Check basic rounding
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "", "160355379", "2023-01-20 11:59 PM EST", "87.261")
        getter = ZybooksRowGetter(row)

        self.assertEqual("austi121", getter.netid)
        self.assertEqual("8.73", getter.points_grade)
        self.assertEqual("#", getter.end_of_line_indicator)

        # Check that it rounds half up
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "", "160355379", "2023-01-20 11:59 PM EST", "93.85")
        getter = ZybooksRowGetter(row)

        self.assertEqual("austi121", getter.netid)
        self.assertEqual("9.39", getter.points_grade)
        self.assertEqual("#", getter.end_of_line_indicator)
    
    def test_zybooks_to_d2l(self):
        zybooks: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "austi121@msu.edu", "160355379", "2023-01-20 11:59 PM EST", "100")
        d2l = zybooks_to_d2L(zybooks)

        self.assertEqual("austi121", d2l[0])
        self.assertEqual("10.00", d2l[1])
        self.assertEqual("#", d2l[2])

        zybooks: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "austi121@msu.edu", "160355379", "2023-01-20 11:59 PM EST", "12.24")
        d2l = zybooks_to_d2L(zybooks)

        self.assertEqual("austi121", d2l[0])
        self.assertEqual("1.22", d2l[1])
        self.assertEqual("#", d2l[2])
    
    def test_d2l_header(self):
        header = get_d2l_header("MSUCSE331OnsaySpring2023_Activity1_SS23_Algorithm_Analysis_and_Growth_Functions_report_2023-01-21_1310")

        self.assertEqual("Username", header[0])
        self.assertEqual("Activity1_Zybk Points Grade", header[1])
        self.assertEqual("End-Of-Line Indicator", header[2])

        header = get_d2l_header("MSUCSE331OnsaySpring2023_Activity12_SS23_Algorithm_Analysis_and_Growth_Functions_report_2023-01-21_1310")

        self.assertEqual("Username", header[0])
        self.assertEqual("Activity12_Zybk Points Grade", header[1])
        self.assertEqual("End-Of-Line Indicator", header[2])

if __name__ == "__main__":
    unittest.main()
