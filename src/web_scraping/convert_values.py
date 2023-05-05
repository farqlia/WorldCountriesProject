import re

NUMER_PATTERN = re.compile(r"-?\$?([\d,.]+)%?\s*(million|billion)?\s*(\(.*?\))")
ten_powers = {'million': 1_000_000, 'billion': 1_000_000_000}


def convert_to_number(entry):
    number_match = NUMER_PATTERN.match(entry)
    if number_match:
        sign = -1 if entry.startswith("-") else 1
        numeric_string = number_match.group(1)
        numeric_string = numeric_string.replace(",", "")
        try:
            number = float(numeric_string)
            if number_match.group(2):
                number *= ten_powers[number_match.group(2)]
        except ValueError:
            return None
        return sign * number
    return None
