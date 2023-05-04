import pytest
import src.web_scraping.web_scraper as web_scraper


@pytest.fixture()
def html_with_breaks():
    html_paragraph = '''<p>3.3% of GDP (2019) (approximately $2.35 billion)
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
                    2.9% of GDP (2015) (approximately $2.22 billion)</p>'''
    return html_paragraph


@pytest.fixture()
def html_with_strong_tags():
    html_paragraph = '''<p>Amu Darya (shared with Tajikistan [s], Turkmenistan, and Uzbekistan [m])
                <br>
                <strong>note</strong> – [s] after country name indicates river source;</p>'''
    return html_paragraph

@pytest.fixture()
def html_with_nested_paragraphs():
    html_paragraph = '''<p>
    <p>includes main island of Taiwan plus smaller islands nearby and off coast of China's Fujian Province;
    </p> 
    <p>
    <strong>counties:</strong> 
    Changhua, Chiayi, Hsinchu, Hualien, 
    </p>
    <p>
    <strong>cities:</strong> Chiayi, Hsinchu, Keelung
    </p>
    <p>
    <strong>special municipalities:</strong>
    Kaohsiung (city), New Taipei (city), Taipei (city), 
    </p>
    <br>
    <br>
    <strong>note:</strong> Taiwan uses a variety of romanization systems;</p>'''
    return html_paragraph


class TestConvertToDictionary:

    def test_split_on_break_tags(self, html_with_breaks):
        scraped_list = web_scraper.retrieve_paragraph_contents(html_with_breaks)
        assert scraped_list == ['3.3% of GDP (2019) (approximately $2.35 billion)',
                                            '3.2% of GDP (2018) (approximately $2.31 billion)',
                                            '3.3% of GDP (2017) (approximately $2.34 billion)',
                                            '3.1% of GDP (2016) (approximately $2.6 billion)',
                                            '2.9% of GDP (2015) (approximately $2.22 billion)']

    def test_unnest_as_key_value_pair(self, html_with_strong_tags):
        scraped_list = web_scraper.retrieve_paragraph_contents(html_with_strong_tags)
        assert scraped_list == ["Amu Darya (shared with Tajikistan [s], Turkmenistan, and Uzbekistan [m])",
                                {"note": " – [s] after country name indicates river source;"}]

    def test_unnest_with_paragraph_tags(self, html_with_nested_paragraphs):
        scraped_list = web_scraper.retrieve_paragraph_contents(html_with_nested_paragraphs)
        assert scraped_list == ['''includes main island of Taiwan plus smaller islands nearby and off coast of China's Fujian Province;''',
                                {"counties": "Changhua, Chiayi, Hsinchu, Hualien,",
                                 "cities": "Chiayi, Hsinchu, Keelung",
                                 "special municipalities": "Kaohsiung (city), New Taipei (city), Taipei (city),",
                                 "note": "Taiwan uses a variety of romanization systems;"}]





