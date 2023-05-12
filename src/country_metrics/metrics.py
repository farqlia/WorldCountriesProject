import abc
import csv

import numpy as np
from typing import Dict
from functools import partial

from src.web_scraping.web_scraper import get_all_countries
import src.web_scraping.convert_values as convert_values
from typing import List
import pandas as pd


def create_empty_df(columns, dtype=float):
    df = pd.DataFrame(columns=columns,
                      index=get_all_countries(),
                      dtype=dtype)
    return df


def parametrize_csv_saving(destructure_method, conversion_function):

    def save(path, fields: List[str], country_samples, *args, **kwargs):

        fieldnames = ['country'] + fields
        with open(path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for country in get_all_countries():
                rates = destructure_method(country_samples[country], *args, **kwargs) if country in country_samples else {}
                converted_fields = {var: convert_values.convert_or_get_nan(conversion_function,
                                                                           rates.get(var, []))[0] for var in fields}
                converted_fields.update({'country': country})
                writer.writerow(converted_fields)

    return save

