import numpy as np
import pytest

import src.web_scraping.convert_values as convert_values

# Each of these test cases should be converted to values
# From these also only numbers
# "6.6 deaths/1,000 population (2023 est.)"
# "38.6% of household expenditures (2018 est.)"
# "96.875 million metric tonnes of CO2 (2019 est.)"
# "9.6% of GDP (2020)"
# "79% of population"
# 13.604 million Btu/person (2019 est.) Data represented includes both the Gaza Strip and West Bank
# 26.786 million Btu/person (2019 est.)
# 57.2 deaths/1,000 live births
# -26.2 migrant(s)/1,000 population (2023 est.)


class TestConvertStringToNumber:

    @pytest.mark.parametrize("case,expected",
                             [("-1", -1),
                                ("123", 123), ("-1,734", -1734),
                              ("1,434,542", 1434542),
                              ("1.99", 1.99)])
    def test_for_valid_cases(self, case, expected):
        assert convert_values.convert_string_to_number(case) == expected

    @pytest.mark.parametrize("case", ["$1.99"])
    def test_for_invalid_cases(self, case):
        assert not convert_values.convert_string_to_number(case)


class TestConvertToNumber:

    @pytest.mark.parametrize("case,value",
                             list(zip(
                                 [
                                     "864,000 (2021 est.)",
                                     "54% (2021 est.)",
                                     "1.183 million (2021 est.)",
                                     "389,063,826 (2021 est.)",
                                     "55,069 (2021 est.)",
                                     "5.3 billion (2022 est.)",
                                     "$1.264 billion (2019 est.)",
                                     "-$31.19 million (2020 est.)"
                                 ],
                                [864_000, 54, 1_183_000, 389_063_826,
                                 55_069, 5_300_000_000, 1_264_000_000,
                                  -31_190_000
                                ])))
    def test_for_valid_cases(self, case, value):
        assert convert_values.convert_to_number(case) == value


class TestQuantityOf:

    @pytest.mark.parametrize("case,expected",
                             [("38.6% of household expenditures (2018 est.)", (38.6, "household expenditures")),
                              ("96.875 million metric tonnes of CO2 (2019 est.)", (96_875_000, "CO2")),
                              ("9.6% of GDP (2020)", (9.6, "GDP")),
                              ("79% of population", (79, "population"))])
    def test_for_valid_cases(self, case, expected):
        assert convert_values.convert_quantity_of(case) == expected


class TestFraction:

    @pytest.mark.parametrize("case,expected",
        [("6.6 deaths/1,000 population (2023 est.)", (6.6, "deaths/population")),
         ("26.786 million Btu/person (2019 est.)", (26_786_000, "Btu/person")),
         ("-26.2 migrant(s)/1,000 population (2023 est.)", (-26.2, "migrant(s)/population")),
         ("57.2 deaths/1,000 live births", (57.2, "deaths/live births"))]
    )
    def test_convert_fractions(self, case, expected):
        assert convert_values.convert_fraction(case) == expected


class TestConvertOrGetNone:

    @pytest.mark.parametrize("func,arg", [(convert_values.convert_to_number, "NA"),
                                      (convert_values.convert_quantity_of, "NA"),
                                      (convert_values.convert_fraction, "NA")])
    def test_result_is_none(self, func, arg):
        assert convert_values.convert_or_get_nan(func, arg) == [np.NAN]

    @pytest.mark.parametrize("func,arg,expected", [(convert_values.convert_to_number, "123.123", 123.123),
                                          (convert_values.convert_quantity_of, "38.6% of household expenditures (2018 est.)", (38.6, "household expenditures")),
                                          (convert_values.convert_fraction, "6.6 deaths/1,000 population (2023 est.)", (6.6, "deaths/population"))])
    def test_result_is_not_none(self, func, arg, expected):
        assert convert_values.convert_or_get_nan(func, arg) == expected