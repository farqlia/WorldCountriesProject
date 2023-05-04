import pytest
import requests

import src.web_scraping.web_scraper as web_scraper
import bs4
from pathlib import Path

html_doc = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<main id="main-content">
    <ul>
        <li>
            <h2>
                <a>Afganistan</a>
            </h2>
            <p>
                3.3% of GDP (2019) (approximately $2.35 billion)
                <br>
                <br>
                3.2% of GDP (2018) (approximately $2.31 billion)
                <br>
                <br>
                3.3% of GDP (2017) (approximately $2.34 billion)
                <br>
                <br>
                3.1% of GDP (2016) (approximately $2.6 billion)
                <br>
                <br>
                2.9% of GDP (2015) (approximately $2.22 billion)
            </p>
        </li>
        <li>
            <h2>
                <a>Albania</a>
            </h2>
            <p>
                1.4% of GDP (2021 est.)
                <br>
                <br>
                1.3% of GDP (2020)
                <br>
                <br>
                1.5% of GDP (2019) (approximately $360 million)
                <br>
                <br>
                1.3% of GDP (2018) (approximately $330 million)
                <br>
                <br>
                1.1% of GDP (2017) (approximately $290 million)
            </p>
        </li>
    </ul>
</main>
</body>
</html>
'''


def test_for_correct_retrieving_paragraph_content_from_webpage():
    data = web_scraper.retrieve_paragraph_contents(html_doc)
    countries = [row.country for row in data]
    assert countries == ['Afganistan', 'Albania']


@pytest.fixture()
def countries():
    response = requests.get("https://www.cia.gov/the-world-factbook/field/death-rate/")
    countries = web_scraper.get_all_countries(response.content)
    return countries


def test_for_extracting_countries_names(countries):
    print(countries)
    # these are not countries so we won't want them
    assert 'World' in countries
    assert 'West Bank' in countries
    assert len(countries) == 253


def test_filter_out_differing_countries(countries):
    print()
    differences = set(countries).difference(set(web_scraper.get_true_countries()))
    differences_2 = set(web_scraper.get_true_countries()).difference(set(countries))
    for diff in differences:
        print(diff)
    print("---------------------------")
    for diff in differences_2:
        print(diff)


def test_filter_out_true_country_names():
    web_scraper.filter_out_true_countries([])