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
    assert data[0].country == 'Afganistan'
    assert list(data[0].paragraph_content) == [
        '3.3% of GDP (2019) (approximately $2.35 billion)',
        '3.2% of GDP (2018) (approximately $2.31 billion)',
        '3.3% of GDP (2017) (approximately $2.34 billion)',
        '3.1% of GDP (2016) (approximately $2.6 billion)',
        '2.9% of GDP (2015) (approximately $2.22 billion)'
    ]


@pytest.fixture()
def countries():
    response = requests.get("https://www.cia.gov/the-world-factbook/field/death-rate/")
    countries = web_scraper.retrieve_countries(response.content)
    return countries


def test_for_extracting_countries_names(countries):
    # these are not countries so we won't want them
    assert 'World' in countries
    assert 'European Union' in countries
    assert 'West Bank' in countries
    assert len(countries) == 253


def test_filter_out_true_country_names(countries):
    filtered_countries = web_scraper.filter_out_true_countries(countries)
    assert 'World' not in filtered_countries
    assert 'West Bank' not in filtered_countries
    assert 'European Union' not in filtered_countries


def test_get_true_countries():
    print(len(web_scraper.get_all_countries()))
    print(web_scraper.get_all_countries())


# Not a real tests
def test_filter_out_differing_countries(countries):
    print()
    differences = set(countries).difference(set(web_scraper.get_all_countries()))
    differences_2 = set(web_scraper.get_all_countries()).difference(set(countries))
    for diff in differences:
        print(diff)
    print("---------------------------")
    for diff in differences_2:
        print(diff)

    print("----------------------------")
    intersection = set(countries).intersection(set(web_scraper.get_all_countries()))
    print(len(intersection))
    for c in intersection:
        print(c)


def test_for_stripped_strings():
    soup = bs4.BeautifulSoup(html_doc)
    html_fragments = soup.stripped_strings
    print(html_fragments)

    for fragment in html_fragments:
        print(fragment)
