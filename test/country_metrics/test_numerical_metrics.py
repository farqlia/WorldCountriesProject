import numpy as np
import pandas as pd
import pytest

import src.country_metrics.numerical_metrics as numerical_metrics
import src.web_scraping.web_scraper as web_scraper
# import pandas as pd
from src.global_vars import NUMBER_OF_COUNTRIES
import pandas.testing as pd_test


class TestGetCountryInfantMortalityRate:

    @pytest.fixture
    def samples(self):
        arguments = [web_scraper.CountrySample(
                        "Angola",
                        ["total:", "57.2 deaths/1,000 live births",
                         "male:", "62.37 deaths/1,000 live births",
                         "female:", "51.87 deaths/1,000 live births (2023 est.)"]
        ),
                     web_scraper.CountrySample(
                         "Anguilla",
                         ["total:", "3.02 deaths/1,000 live births",
                          "male:", "3.94 deaths/1,000 live births",
                          "female:", "2.08 deaths/1,000 live births (2023 est.)"]
                     )]
        return arguments

    def test_get_rate(self, samples):
        expected = pd.DataFrame(data=[[57.2, 62.37, 51.87], [3.02, 3.94, 2.08]],
                                index=['Angola', 'Anguilla'],
                                columns=["total", "male", "female"])
        actual = numerical_metrics.get_country_infant_mortality_rate(samples)
        assert len(actual) == NUMBER_OF_COUNTRIES
        pd_test.assert_series_equal(actual.loc['Angola'], expected.loc['Angola'])


    @pytest.fixture
    def sample_with_none(self):
        return web_scraper.CountrySample(
            "Angola",
            ["total:", "NA",
             "male:", "NA",
             "female:", "NA"]
        )

    def test_case_with_nan(self, sample_with_none):
        df = numerical_metrics.get_country_infant_mortality_rate([sample_with_none])
        assert all(np.isnan(df.loc['Angola']))


class TestPopulationGrowthRate:

    @pytest.fixture()
    def samples(self):
        arguments = [web_scraper.CountrySample(
            "Afghanistan", ["2.26% (2023 est.)"]
        ), web_scraper.CountrySample("Estonia", ["-0.74% (2023 est.)"])]
        return arguments

    def test_get_population_growth_rate(self, samples):
        expected = pd.DataFrame(data=[[2.26], [-0.74]],
                                index=["Afghanistan", "Estonia"],
                                columns=["rate"])
        actual = numerical_metrics.get_population_growth_rate(samples)
        pd_test.assert_frame_equal(actual.loc[["Afghanistan", "Estonia"]],
                                   expected)

    @pytest.mark.xfail("Index is not present")
    @pytest.mark.parametrize("case", [
        web_scraper.CountrySample("European Union", "(2021 est.) 0.10%"),
        web_scraper.CountrySample("Cocos (Keeling) Islands", "NA")
    ])
    def test_malformed_or_none(self, case):
        assert not numerical_metrics.get_population_growth_rate([case]).loc[case.country]
