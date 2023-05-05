import pytest

import src.web_scraping.convert_values as convert_values

# Each of these test cases should be converted to values
test_cases = [
    "864,000 (2021 est.)",
    "54% (2021 est.)",
    "1.183 million (2021 est.)",
    "389,063,826 (2021 est.)",
    "55,069 (2021 est.)",
    "5.3 billion (2022 est.)",
    "$1.264 billion (2019 est.)",
    "-$31.19 million (2020 est.)"
]

# From these also only numbers
# "6.6 deaths/1,000 population (2023 est.)"
# "38.6% of household expenditures (2018 est.)"
# "96.875 million metric tonnes of CO2 (2019 est.)"
# "9.6% of GDP (2020)"
# "79% of population"


class TestConvertToNumber:

    @pytest.mark.parametrize("case,value",
                             list(zip(test_cases,
                                      [864_000, 54, 1_183_000, 389_063_826,
                                       55_069, 5_300_000_000, 1_264_000_000,
                                       -31_190_000])))
    def test_for_valid_cases(self, case, value):
        assert convert_values.convert_to_number(case) == value