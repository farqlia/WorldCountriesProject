from src.country_metrics.metrics import CountryMetric
import src.web_scraping.destructuring as destructuring
import src.web_scraping.convert_values as convert_values
from typing import List
from src.web_scraping.web_scraper import CountrySample


def get_country_infant_mortality_rate(country_sample: List[CountrySample]):
    fields = ['total', 'male', 'female']
    metric = CountryMetric(destructuring.destructure_list_like,
                           convert_values.convert_to_number,
                           fields)
    return metric.get_metric_df(country_sample)


def get_population_growth_rate(country_sample: List[CountrySample]):
    fields = ["rate"]
    metric = CountryMetric(destructuring.destructure_text_paragraph,
                           convert_values.convert_to_number,
                           fields)
    return metric.get_metric_df(country_sample)


def get_age_structure(country_sample: List[CountrySample]):
    fields = ['0-14 years', '15-64 years', '65 years and over']
    metric = CountryMetric(destructuring.destructure_list_like,
                           convert_values.convert_to_number,
                           fields)
    return metric.get_metric_df(country_sample)


def get_birth_rate(country_sample: List[CountrySample]):
    fields = ["rate"]
    metric = CountryMetric(destructuring.destructure_text_paragraph,
                           convert_values.convert_to_number,
                           fields)
    return metric.get_metric_df(country_sample)


def get_migration_rate(country_sample: List[CountrySample]):
    fields = ["rate"]
    metric = CountryMetric(destructuring.destructure_text_paragraph,
                           convert_values.convert_fraction,
                           fields)
    return metric.get_metric_df(country_sample)