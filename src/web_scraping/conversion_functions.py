import logging
import re

import numpy as np

from src.logging_errors.logging_setup import log_on_none
from src.web_scraping.destructuring_functions import HEADER_PATTERN

NUMER_PATTERN = re.compile(r"-?\$?([\d,.]+)%?\s*(million|billion)?")
ten_powers = {'million': 1_000_000, 'billion': 1_000_000_000}
QUANTITY_OF_PATTERN = re.compile(r"(.*?) of ([\w\s]+\w)")
FRACTION_PATTERN = re.compile(r"(.*)\s(.*?)/([\d,]+)?\s?([\s\w]+\w)")
REGION_PATTERN = re.compile("(Africa|North America|Caribbean|South America|Asia|Europe|Middle East|Oceania)")
CONTINENT_PATTERN = re.compile(r"(?P<continent>[\w\s]+) \(\d+\)")
COUNTRIES_PATTERN = re.compile(r"\w[\w\s-]+\w")


def convert_or_return_nan(conversion_function, *args):
    if not args[0]:
        return np.NAN
    result = conversion_function(*args)
    if result is None:
        result = np.NAN
    return result


def convert_string_to_number(numeric_string: str, mil_or_bil=None):
    numeric_string = numeric_string.replace(",", "")
    try:
        number = float(numeric_string)
        if mil_or_bil:
            number *= ten_powers[mil_or_bil]
    except ValueError:
        return None
    return number


@log_on_none(logging.WARNING)
def convert_to_number(entry: str):
    number_match = NUMER_PATTERN.match(entry)
    if number_match:
        sign = -1 if entry.startswith("-") else 1
        return sign * convert_string_to_number(number_match.group(1), number_match.group(2))
    return None


@log_on_none(logging.WARNING)
def convert_quantity_of(entry: str):
    quantity_match = QUANTITY_OF_PATTERN.match(entry)
    if quantity_match:
        number = convert_to_number(quantity_match.group(1))
        return number
    return None


@log_on_none(logging.WARNING)
def convert_fraction(entry: str):
    fraction_match = FRACTION_PATTERN.match(entry)
    if fraction_match:
        number = convert_to_number(fraction_match.group(1))
        return number
    return None


def extract_location(entry: str):
    location_match = REGION_PATTERN.search(entry)
    return location_match.group(1) if location_match else None


def get_continent_and_countries(paragraph):
    split_on_colon = paragraph.split(":")
    continent = CONTINENT_PATTERN.match(split_on_colon[0]).group('continent')
    countries = list(map(lambda c: c.group(), filter(lambda c: c is not None,
                            map(lambda s: COUNTRIES_PATTERN.search(s),
                                split_on_colon[1].split(',')))))
    return continent.strip(), countries


def extract_header(entry: str):
    header_match = re.search(HEADER_PATTERN, entry)
    return header_match.group(1) if header_match else None