import re
import typing

import bs4
from dataclasses import dataclass
from bs4 import Tag
import json
from src.global_vars import DATA_PATH

@dataclass
class CountryData:
    country: str
    paragraph_content: Tag


def retrieve_paragraph_contents(html):
    soup = bs4.BeautifulSoup(html)
    list_of_countries_data = soup.body.find('main', attrs={'id': 'main-content'}).find('ul').find_all('li')
    country_paragraphs = []
    for row in list_of_countries_data:
        country = row.a.contents[0]
        paragraph = row.p
        country_paragraphs.append(CountryData(country, paragraph))

    return country_paragraphs


def get_all_countries(html):
    country_paragraphs = retrieve_paragraph_contents(html)
    return [row.country for row in country_paragraphs]


def get_true_countries():
    with open(DATA_PATH.joinpath('countries.json')) as f:
        world_countries_codes = json.load(f)
        world_countries = [entry['name'] for entry in world_countries_codes]
        return world_countries


def filter_out_true_countries(countries):
    pass









