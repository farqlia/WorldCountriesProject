import numpy as np
import pandas as pd
import pytest

import src.country_metrics.save_metrics
import src.country_metrics.save_metrics as save_metrics
import src.web_scraping.web_scraper as web_scraper
# import pandas as pd
from src.global_vars import NUMBER_OF_COUNTRIES
import pandas.testing as pd_test
from src.global_vars import DATA_PATH

# TODO : change path to where files are saved


def open_from_csv(metric):
    return pd.read_csv(DATA_PATH / f"{metric}.csv").set_index('country')


class TestGetCountryInfantMortalityRate:

    @pytest.fixture
    def samples(self):
        arguments = {
                        "Angola":
                        ["total:", "57.2 deaths/1,000 live births",
                         "male:", "62.37 deaths/1,000 live births",
                         "female:", "51.87 deaths/1,000 live births (2023 est.)"],
                         "Anguilla":
                         ["total:", "3.02 deaths/1,000 live births",
                          "male:", "3.94 deaths/1,000 live births",
                          "female:", "2.08 deaths/1,000 live births (2023 est.)"]
                     }
        return arguments

    def test_get_rate(self, samples):
        expected = pd.DataFrame(data=[[57.2, 62.37, 51.87], [3.02, 3.94, 2.08]],
                                index=['Angola', 'Anguilla'],
                                columns=["total", "male", "female"])
        save_metrics.save_infant_mortality_rate(samples)
        actual = open_from_csv("infant_mortality_rate")
        pd_test.assert_series_equal(actual.loc['Angola'], expected.loc['Angola'])


    @pytest.fixture
    def sample_with_none(self):
        return {"Angola":
            ["total:", "NA",
             "male:", "NA",
             "female:", "NA"]
           }

    def test_case_with_nan(self, sample_with_none, get_im_path, mocker):
        mocker.patch.object('src.country_metrics.save_metrics.get_path', get_im_path)
        save_metrics.save_infant_mortality_rate([sample_with_none])
        df = open_from_csv(get_im_path)
        assert all(np.isnan(df.loc['Angola']))


class TestPopulationGrowthRate:

    @pytest.fixture()
    def samples(self):
        arguments = {
            "Afghanistan": ["2.26% (2023 est.)"],
        "Estonia": ["-0.74% (2023 est.)"]}
        return arguments

    def test_get_population_growth_rate(self, samples):
        expected = pd.DataFrame(data=[[2.26], [-0.74]],
                                index=["Afghanistan", "Estonia"],
                                columns=["rate"])
        save_metrics.save_population_growth_rate(samples)
        actual = open_from_csv("population_growth_rate")
        pd_test.assert_frame_equal(actual.loc[["Afghanistan", "Estonia"]],
                                   expected, check_names=False)

    @pytest.mark.skip("Index is not present")
    @pytest.mark.parametrize("case",
        [{"European Union": ["(2021 est.) 0.10%"]},
        {"Cocos (Keeling) Islands": ["NA"]}]
    )
    def test_malformed_or_none(self, case):
        save_metrics.save_infant_mortality_rate([case])
        df = open_from_csv("population_growth_rate")
        assert not df.loc[case.keys()[0]]
