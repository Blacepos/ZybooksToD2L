#!/bin/python3
"""
This program converts all csv files in the directory "./imports" from Zybooks to
D2L format, saving the results in "./exports".
This file makes as few assumptions as possible in order to be
as correct as possible. Any formatting that I suspect may change in future
semesters are in `assumptions.py`.
"""

import os
from typing import Generator, List
import csv
from itertools import islice
from multiprocessing import Pool

from assumptions import ZybooksRow, D2LRow, get_d2l_header, get_d2l_filename,\
    zybooks_to_d2l, ZYBOOKS_ROW_EXPECTED_LEN


def read_zybooks(filename: str) -> Generator[ZybooksRow, None, None]:
    """
    Read a csv in Zybooks format to a Python object
    :param filename: the filename to read from
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None)

        for row in reader:
            if len(row) <= 1:
                continue
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


def convert(filename: str):
    """
    Convert a single file from zybooks format to d2l format
    :param filename: the zybooks filename to read from
    """
    filepath = os.path.join("imports", filename)

    drows = [zybooks_to_d2l(zrow) for zrow in read_zybooks(filepath)]

    write_d2l(os.path.join("exports", get_d2l_filename(filename)), drows)


def main():

    # TODO: process files in parallel

    with Pool() as pool:
        pool.map(convert, os.listdir("imports"))


if __name__ == "__main__":
    main()
