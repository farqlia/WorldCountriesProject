import abc

import numpy as np

from src.web_scraping.web_scraper import CountrySample, get_all_countries
import src.web_scraping.convert_values as convert_values
from typing import List
import pandas as pd


def create_empty_df(columns, dtype=float):
    df = pd.DataFrame(columns=columns,
                      index=get_all_countries(),
                      dtype=dtype)
    return df


class CountryMetric:

    def __init__(self, destructure_method, conversion_function, fields: List[str]):
        self.destructure_method = destructure_method
        self.conversion_function = conversion_function
        self.fields = fields

    def get_metric_df(self, country_samples: List[CountrySample]):

        df = create_empty_df(self.fields)
        for sample in country_samples:
            rates = self.destructure_method(sample.paragraph_content)
            for field in self.fields:
                df.loc[sample.country, field] = convert_values.convert_or_get_nan(self.conversion_function, rates[field])[0]

        return df
