import logging
import re

import numpy as np

from src.logging_errors.logging_setup import log_on_none

NUMER_PATTERN = re.compile(r"-?\$?([\d,.]+)%?\s*(million|billion)?")
ten_powers = {'million': 1_000_000, 'billion': 1_000_000_000}
QUANTITY_OF_PATTERN = re.compile(r"(.*?) of ([\w\s]+\w)")
FRACTION_PATTERN = re.compile("(.*)\s(.*?)/([\d,]+)?\s?([\s\w]+\w)")


def convert_or_get_nan(conversion_function, *args):
    result = conversion_function(*args)
    if not result:
        result = [np.NAN]
    return result


def convert_string_to_number(numeric_string, mil_or_bil=None):
    numeric_string = numeric_string.replace(",", "")
    try:
        number = float(numeric_string)
        if mil_or_bil:
            number *= ten_powers[mil_or_bil]
    except ValueError:
        return None
    return number


@log_on_none(logging.WARNING)
def convert_to_number(entry):
    number_match = NUMER_PATTERN.match(entry)
    if number_match:
        sign = -1 if entry.startswith("-") else 1
        return sign * convert_string_to_number(number_match.group(1), number_match.group(2)),
    return None


@log_on_none(logging.WARNING)
def convert_quantity_of(entry):
    quantity_match = QUANTITY_OF_PATTERN.match(entry)
    if quantity_match:
        number = convert_to_number(quantity_match.group(1))
        feature = quantity_match.group(2)
        return number, feature
    return None


@log_on_none(logging.WARNING)
def convert_fraction(entry):
    fraction_match = FRACTION_PATTERN.match(entry)
    if fraction_match:
        number = convert_to_number(fraction_match.group(1))
        feature = fraction_match.group(2) + "/" + fraction_match.group(4)
        return number, feature
    return None
