import csv
import re
import typing

import bs4
from dataclasses import dataclass
from src.global_vars import DATA_PATH

@dataclass
class CountrySample:
    country: str
    paragraph_content: typing.List[str]


def retrieve_paragraph_contents(http_response_content):
    soup = bs4.BeautifulSoup(http_response_content, 'html.parser')
    list_of_countries_data = soup.body.find('main', attrs={'id': 'main-content'}).find('ul').find_all('li')
    country_paragraphs = []
    for row in list_of_countries_data:
        country = row.a.contents[0]
        paragraph = row.p.stripped_strings
        country_paragraphs.append(CountrySample(country, paragraph))

    return country_paragraphs


def retrieve_countries(html):
    country_paragraphs = retrieve_paragraph_contents(html)
    countries = [row.country for row in country_paragraphs]
    countries.remove('World')
    return countries


def get_all_countries():
    with open(DATA_PATH.joinpath('export.csv')) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        world_countries = [row[0] for row in reader]
        world_countries.remove('Tokelau')
        return world_countries


def filter_out_true_countries(countries):
    return list(set(countries).intersection(set(get_all_countries())))









