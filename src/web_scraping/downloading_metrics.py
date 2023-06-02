import pandas as pd
import requests
from src.web_scraping.string_formatter import StringFormatter
import src.web_scraping.web_scraper as web_scraper
import src.country_metrics.save_metrics as save_metrics
from typing import List
from pathlib import Path
from src.global_vars import DATA_PATH


CATEGORICAL_METRICS = [
     'geographic overview', 'food insecurity'
]

NUMERICAL_METRICS = ['infant mortality rate', 'population growth rate',
    'age structure', 'birth rate', 'net migration rate',
    'alcohol consumption per capita', 'child marriage',
    'contraceptive prevalence rate',
    'currently married women ages 15 49', 'death rate',
    'education expenditures', 'gdp official exchange rate',
    'gini index coefficient distribution of family income',
    'labor force by occupation', 'life expectancy at birth',
    'literacy', 'maternal mortality ratio',
    'mothers mean age at first birth',
    'obesity adult prevalence rate', 'physicians density',
    'population below poverty line',
    'school life expectancy primary to tertiary education',
    'sex ratio', 'tobacco use', 'total fertility rate',
    'unemployment rate', 'current health expenditure', 'median age', 'dependency ratios',
    'drinking water source', 'population', 'labor force by occupation',
    'budget surplus or deficit', 'energy consumption per capita',
    'gdp composition by end use', 'industrial production growth rate',
     'taxes and other revenues', 'internet users', 'real gdp per capita']


class Downloader:

    def __init__(self):
        self.url_formatter = StringFormatter.from_base("https://www.cia.gov/the-world-factbook")
        self.url_formatter = self.url_formatter.append("field/{field}/")

    def download(self, field: str):
        field = field.replace(r' ', '-')
        response = requests.get(self.url_formatter.put_params(field=field))
        if response:
            countries_dict = web_scraper.retrieve_paragraph_contents(response.content)
            saving_function = getattr(save_metrics, "save_" + field.replace("-", "_"))
            saving_function(countries_dict)
        else:
            raise ValueError(f"Couldn't download: {field}")


def open_metric(metric: str):
    return pd.read_csv(DATA_PATH / (metric.replace(" ", "_") + ".csv"), na_values='nan').set_index("country")


def download_metrics(metrics: List[str]):
    downloader = Downloader()
    for metric in metrics:
        try:
            downloader.download(metric)
        except ValueError as err:
            print(err)
            continue


def assert_all_are_downloaded(metrics):
    for metric in metrics:
        assert Path(DATA_PATH.joinpath(f"{metric.replace(' ', '_')}.csv")).exists()
