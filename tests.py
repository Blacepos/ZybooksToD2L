import unittest
from zybooks_to_d2l import *
from assumptions import *

class Tests(unittest.TestCase):
    def test_zybooks_to_d2l(self):
        # Check that it at least works
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "austi121@msu.edu", "160355379", "2023-01-20 11:59 PM EST", "100")
        netid, points_grade, end_of_line_indicator = zybooks_to_d2l(row)

        self.assertEqual("austi121", netid)
        self.assertEqual("10.00", points_grade)
        self.assertEqual("#", end_of_line_indicator)

        # Check basic rounding
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "", "160355379", "2023-01-20 11:59 PM EST", "87.261")
        netid, points_grade, end_of_line_indicator = zybooks_to_d2l(row)

        self.assertEqual("austi121", netid)
        self.assertEqual("8.73", points_grade)
        self.assertEqual("#", end_of_line_indicator)

        # Check that it rounds half up
        row: ZybooksRow = ("Austin", "Joshua", "austi121@msu.edu", "", "160355379", "2023-01-20 11:59 PM EST", "93.85")
        netid, points_grade, end_of_line_indicator = zybooks_to_d2l(row)

        self.assertEqual("austi121", netid)
        self.assertEqual("9.39", points_grade)
        self.assertEqual("#", end_of_line_indicator)
    
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
