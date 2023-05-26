import bs4
import re

COUNTRY_NAME_PATTERN = re.compile(r"[-,A-Za-z\s]+")


def retrieve_paragraph_contents(http_response_content: bytes):
    soup = bs4.BeautifulSoup(http_response_content, 'html.parser')
    list_of_countries_data = soup.body.find('main', attrs={'id': 'main-content'}).find('ul').find_all('li')
    country_paragraphs = {}
    for li_tag in list_of_countries_data:
        # It needs to have an <a></a> tag
        if has_link_tag(li_tag):
            country = get_country_name(li_tag)
            paragraph = li_tag.p.stripped_strings
            country_paragraphs[country] = paragraph

    return country_paragraphs


def has_link_tag(li_tag):
    return li_tag.a is not None


def get_country_name(li_tag):
    country = COUNTRY_NAME_PATTERN.search(li_tag.a.contents[0]).group().strip()
    # Some countries have names like: 'Korea, North' so we convert them to form 'North Korea'
    if "," in country:
        split_name = country.split(",")
        country = (split_name[1] + " " + split_name[0]).strip()
    return country
