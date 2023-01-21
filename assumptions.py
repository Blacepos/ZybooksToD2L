"""
This file contains all of the code that I suspect may require changing from semester to semester.
For example: The name of the column D2L expects in the output csv.
"""

import re
from typing import Tuple
import util

# The exact format we expect the Zybooks csv to be in (truncating everything after "Percent Grade")
ZybooksRow = Tuple[str, str, str, str, str, str, str]

# The exact format we expect the D2L csv to be in
D2LRow = Tuple[str, str, str]

ZYBOOKS_ROW_EXPECTED_LEN = 7

class ZybooksFilenameInvalidFormat(Exception):
    pass
class ZybooksFilenameUnexpectedMatch(Exception):
    pass

def get_activity_from_filename(filename: str) -> str:
        # match "Activity" plus 1 or 2 digits, but not 3
    result = re.search("Activity\\d{1,2}", filename)
    if result is not None:
        activity = result.group()

        # It technically isn't possible for it to not be `str`, but I'm being extra careful because
        # I have trust issues with dynamic typing
        if isinstance(activity, str):
            return activity
        
        raise ZybooksFilenameUnexpectedMatch("`result.group()` returned an unexpected type: `{}`. Value: `{}`".format(type(activity), activity))
    
    raise ZybooksFilenameInvalidFormat(f"Expected csv filename to contain the string \"ActivityXX\" to identify the activity name. Got this instead: \"{filename}\"")

def get_d2l_filename(zybooks_filename: str) -> str:
    activity = get_activity_from_filename(zybooks_filename)
    return activity + "_D2L.csv"


# "MSUCSE331Onsay ... .csv" -> "Activity1_Zybk Points Grade"
def get_d2l_header(filename: str) -> Tuple[str, str, str]:
    activity = get_activity_from_filename(filename)
    return ("Username", activity + "_Zybk Points Grade", "End-Of-Line Indicator")



class ZybooksRowInvalidLength(Exception):
    pass
class ZybooksRowNoMsuEmail(Exception):
    pass
class ZybooksRowPercentGradeNotInRange(Exception):
    pass
class ZybooksRowInvalidType(Exception):
    pass

class ZybooksRowGetter:
    """
    Validate and provide easy access to specific attributes from a row of a Zybooks csv
    """

    PRIMARY_EMAIL_IDX = 2
    SCHOOL_EMAIL_IDX = 3
    PERCENT_GRADE_IDX = 6

    def __init__(self, row: ZybooksRow) -> None:

        # performs regex matching and type checking to make sure the columns we're concerned with
        # are correct
        self.netid, self.points_grade, self.end_of_line_indicator = self._parse_row(row)

    def _parse_row(self, row: ZybooksRow) -> D2LRow:
        if len(row) < 6:
            raise ZybooksRowInvalidLength(
                "Expected Zybooks row with length of at least 6, got length {}."
                .format(len(row))
            )

        primary = row[ZybooksRowGetter.PRIMARY_EMAIL_IDX]
        school = row[ZybooksRowGetter.SCHOOL_EMAIL_IDX]
        grade = row[ZybooksRowGetter.PERCENT_GRADE_IDX]
        
        try:
            # These should be `str` anyways
            primary = str(primary)
            school = str(school)
            grade = float(grade)

        except ValueError:
            raise ZybooksRowInvalidType("Unable to cast type for a column in Zybooks row")
        
        # make sure there's at least 1 MSU email
        if not util.is_msu_email(school):
            if not util.is_msu_email(primary):
                raise ZybooksRowNoMsuEmail("Student does not appear to have an MSU email")
            
            netid = util.get_net_id_from_email(primary)
        else:
            netid = util.get_net_id_from_email(school)
        
        if grade > 100 or grade < 0:
            
            raise ZybooksRowPercentGradeNotInRange(f"Student grade column is not in range [0,100]. Got: {grade}")
    
        points_grade = "{:.2f}".format(util.round_half_up(grade / 10, 2))

        return netid, points_grade, "#"
