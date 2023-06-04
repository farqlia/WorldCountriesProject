import abc
import csv
import os

from src.web_scraping.save_countries import get_all_countries, save_countries
import src.web_scraping.conversion_functions as convert_values
from typing import List
from src.global_vars import DATA_PATH


def parametrize_csv_saving(destructure_method, conversion_function):

    def save_to_csv(path, fields: List[str], country_samples, *args, **kwargs):

        fieldnames = ['country'] + fields
        with open(path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for country in get_all_countries():
                values = destructure_method(country_samples[country], *args, **kwargs) \
                    if country in country_samples else {}
                # Either extract information or write nan
                converted_fields = {var: convert_values.convert_or_return_nan(conversion_function,
                                                                              values.get(var, None)) for var in fields}
                converted_fields.update({'country': country})
                writer.writerow(converted_fields)

    return save_to_csv

