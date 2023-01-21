import re
from math import floor, ceil

def is_email(text: str) -> bool:
    # Source: https://regexr.com/3e48o
    return re.match("^[\\w\\-\\.]+@([\\w-]+\\.)+[\\w\\-]{2,4}$", text) is not None

def is_msu_email(text: str) -> bool:
    if is_email(text):
        return text[text.index('@')+1:].lower() == "msu.edu"
    return False

def get_net_id_from_email(email: str) -> str:
    return email[:email.index('@')]

# Python's built-in rounding differs from Excel
# Source: https://realpython.com/python-rounding/#rounding-half-up
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return floor(n*multiplier + 0.5) / multiplier
