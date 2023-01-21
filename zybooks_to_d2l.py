#!/bin/python3
"""
This program converts all csv files in the directory "./imports" from Zybooks to D2L format, saving
the results in "./exports".
This file makes as few assumptions as can be resonably justified in order to be as correct as
possible. Any formatting that I suspect may change in future semesters are in `assumptions.py`.
"""

import os
from typing import Generator, List
import csv
from itertools import islice

from assumptions import ZybooksRow, D2LRow, get_d2l_header, get_d2l_filename, ZybooksRowGetter, ZYBOOKS_ROW_EXPECTED_LEN

def read_zybooks(filename: str) -> Generator[ZybooksRow, None, None]:
    """
    Read a csv in Zybooks format to a Python object
    :param filename: the filename to read from
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None)

        for row in reader:
            yield tuple(islice(row, ZYBOOKS_ROW_EXPECTED_LEN))

def write_d2l(filename: str, data: List[D2LRow]):
    """
    Write a Python object to a csv file to be upload to D2L
    :param filename: the path to write the csv data to
    :param data: the rows of data corresponding to the D2L CSV
    """
    with open(filename, 'w') as file:
        writer = csv.writer(file)

        writer.writerow(get_d2l_header(filename))

        writer.writerows(data)

def zybooks_to_d2L(row: ZybooksRow) -> D2LRow:
    """
    Map a single row from Zybooks format to D2L
    :param row: A single row from the Zybooks CSV
    """
    getter = ZybooksRowGetter(row)
    return (getter.netid, getter.points_grade, getter.end_of_line_indicator)



def main():

    # TODO: process files in parallel

    for filename in os.listdir("imports"):
        filename = os.path.join("imports", filename)
        
        drows = [zybooks_to_d2L(zrow) for zrow in read_zybooks(filename)]

        write_d2l(os.path.join("exports", get_d2l_filename(filename)), drows)


if __name__ == "__main__":
    main()
