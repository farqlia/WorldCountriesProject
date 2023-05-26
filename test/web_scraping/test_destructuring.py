import bs4
import pytest

import src.web_scraping.destructuring_functions as destructuring

test_case_1_1 = '''
    <p>
        <strong>0-14 years: </strong>
        39.8% (male 7,926,748/female 7,686,979)
        <br>
        <br>
        <strong>15-64 years: </strong>
        57.35% (male 11,413,654/female 11,084,665)
        <br>
        <br>
        <strong>65 years and over: </strong>
        2.85% (2023 est.) (male 515,147/female 604,810)
    </p>
'''

test_case_1_2 = '''
<p>
    <strong>
    Fitch rating: 
    </strong>
    B (2018)
    <br>
    <br>
    <strong>Moody's rating: </strong>
    B3 (2018)
    <br>
    <br>
    <strong>Standard &amp; Poors rating: </strong>
    B (2017)
    <br>
    <br>
    <strong>note: </strong>
    The year refers to the year in which the current credit rating was first obtained.
</p>
'''


def to_list(html):
    soup = bs4.BeautifulSoup(html)
    return soup.stripped_strings


class TestDestructureListLikeParagraph:

    def test_for_valid_case(self):

        expected = {"0-14 years": "39.8% (male 7,926,748/female 7,686,979)",
                    "15-64 years": "57.35% (male 11,413,654/female 11,084,665)",
                    "65 years and over": "2.85% (2023 est.) (male 515,147/female 604,810)"}
        assert expected == destructuring.destructure_list_like(to_list(test_case_1_1))

    def test_for_case_with_note(self):
        expected = {"Fitch rating": "B (2018)",
                    "Moody's rating": "B3 (2018)",
                    "Standard & Poors rating": "B (2017)",
                    "note": "The year refers to the year in which the current credit rating was first obtained."}

        assert expected == destructuring.destructure_list_like(to_list(test_case_1_2))

    def test_for_regular_expression_for_match(self):
        match = destructuring.HEADER_PATTERN.match("improved:")
        assert match.group(1) == "improved"

    def test_for_regular_expression_for_no_match(self):
        no_match = destructuring.HEADER_PATTERN.match("total: 25.3% of population")
        assert not no_match


test_case_2 = '''
<p>
    7.893 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>
    from coal and metallurgical coke: </strong>
    4.158 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>from petroleum and other liquids: </strong>
    3.468 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>from consumed natural gas: </strong>
    267,000 metric tonnes of CO2 (2019 est.)
</p>
'''


class TestDestructureListLikeParagraphWithCaption:

    def test_for_valid_case(self):

        expected = {"from coal and metallurgical coke": "4.158 million metric tonnes of CO2 (2019 est.)",
                    "from petroleum and other liquids": "3.468 million metric tonnes of CO2 (2019 est.)",
                    "from consumed natural gas": "267,000 metric tonnes of CO2 (2019 est.)",
                    "caption": "7.893 million metric tonnes of CO2 (2019 est.)"}
        assert expected == destructuring.destructure_list_like_with_text(to_list(test_case_2))


test_case_3_1 = '''
<p>
<strong>improved: </strong>
    urban: 79% of population
    <br>
    <br>
    rural: 70.8% of population
    <br>
    <br>
    total: 74.7% of population
    <br>
    <br>
<strong>unimproved: </strong>
    urban: 21% of population
    <br>
    <br>
    rural: 29.2% of population
    <br>
    <br>
    total: 25.3% of population (2020 est.)
</p>
'''

test_case_3_2 = '''
<p>
<strong>improved: </strong>
    urban: 79% of population
    <br>
    <br>
    rural: 70.8% of population
    <br>
    <br>
    total: 74.7% of population
    <br>
    <br>
<strong>unimproved: </strong>
    urban: 21% of population
    <br>
    <br>
    rural: 0% of population
    <br>
    <br>
    total: 25.3% of population (2020 est.)
<strong>note: </strong>
    does not include data from the former Western Sahara
</p>
'''

class TestDestructureNestedList:

    # This will not be probably different from the first case
    def test_for_valid_case(self):
        expected = {'improved_urban': '79% of population',
                                 'improved_rural': '70.8% of population',
                                 'improved_total': '74.7% of population', 'unimproved_urban': '21% of population',
                                   'unimproved_rural': '0% of population',
                                   'unimproved_total': '25.3% of population (2020 est.)'
                    }
        assert expected == destructuring.destructure_nested_lists(to_list(test_case_3_1))

    def test_with_note_entry(self):
        assert 'note' in destructuring.destructure_nested_lists(to_list(test_case_3_2))



test_case_4_1 = '''
<p>
7.8% of GDP (2020)
</p>
'''

test_case_4_2 = '''
<p>
    $743.232 million (2020 est.)
    <br>
    <br>
    -$523.837 million (2019 est.)
    <br
    ><br>
    -$664.797 million (2018 est.)
</p>
'''


class TestDestructureParagraph:

    @pytest.mark.parametrize("html,fieldnames,expected",
                             [(to_list(test_case_4_2), ["rate_1", "rate_2", "rate_3"],
                                        {"rate_1": "$743.232 million (2020 est.)",
                                          "rate_2": "-$523.837 million (2019 est.)",
                                          "rate_3": "-$664.797 million (2018 est.)"}),
                              (to_list(test_case_4_1), ["perc"], {"perc": "7.8% of GDP (2020)"})])
    def test_for_valid_cases(self, html, fieldnames, expected):
        assert expected == destructuring.destructure_text_paragraph(html, field_names=fieldnames)


@pytest.mark.parametrize("paragraph",
                         [test_case_1_1, test_case_1_2,
                          test_case_2, test_case_3_1, test_case_4_1,
                          test_case_4_2])
def test_print_each_stripped(paragraph):
    soup = bs4.BeautifulSoup(paragraph)
    html_fragments = soup.stripped_strings
    print()
    for fragment in html_fragments:
        print(fragment, end="|\n")


def test_key_value_conversion():
    arg = "urban: 97.3% of population"
    key, value = destructuring.get_key_value(arg)
    assert key == "urban"
    assert value == "97.3% of population"