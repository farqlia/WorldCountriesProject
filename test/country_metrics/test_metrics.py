import pandas as pd

import src.country_metrics.metrics as metrics
import src.web_scraping.web_scraper as web_scraper
import src.web_scraping.destructuring as destructuring
import src.web_scraping.convert_values as convert_values
import pytest
import pandas.testing as pd_test


class TestCountryMetricToCSV:

    @pytest.fixture()
    def file_path(self, tmp_path):
        path = tmp_path / "metric.csv"
        return path

    @pytest.fixture()
    def get_arg(self):
        return {
                        "Angola":
                        ["total:", "57.2 deaths/1,000 live births",
                         "male:", "62.37 deaths/1,000 live births",
                         "female:", "51.87 deaths/1,000 live births (2023 est.)"]
        ,
                         "Anguilla":
                         ["total:", "3.02 deaths/1,000 live births",
                          "male:", "3.94 deaths/1,000 live births",
                          "female:", "2.08 deaths/1,000 live births (2023 est.)"]
                     }

    @pytest.fixture()
    def get_expected(self):
        return pd.DataFrame(data=[[57.2, 62.37, 51.87], [3.02, 3.94, 2.08]],
                     index=['Angola', 'Anguilla'],
                     columns=["total", "male", "female"])

    def test_save_to_csv_and_retrieve(self, get_arg, file_path, get_expected):
        birth_rates_metric = metrics.parametrize_csv_saving(destructuring.destructure_list_like,
                                                        convert_values.convert_fraction
                                                        )
        birth_rates_metric(file_path, ['total', 'male', 'female'], get_arg)
        actual = pd.read_csv(file_path)
        actual = actual.set_index('country')
        # Index names are not the same
        pd_test.assert_frame_equal(actual.loc[['Angola', 'Anguilla']],
                                   get_expected, check_names=False)

    def test_contains_all_countries(self, file_path):
        metric = metrics.parametrize_csv_saving(destructuring.destructure_list_like,
                                                convert_values.convert_to_number)
        metric(file_path, ['rate'], {})
        actual = pd.read_csv(file_path)
        assert list(actual['country'].values) == web_scraper.get_all_countries()

