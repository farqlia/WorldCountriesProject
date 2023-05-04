import bs4
import pytest


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
    return bs4.BeautifulSoup(html_paragraph)


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
    <p>Kaohsiung (city), New Taipei (city), Taipei (city), </p>
    </p>
    <br>
    <br>
    <strong>note:</strong> Taiwan uses a variety of romanization systems;</p>'''
    return bs4.BeautifulSoup(html_paragraph)


def test_soup_with_nested_paragraphs(html_with_nested_paragraphs):
    print("\n\n")
    expected = ["includes main island of Taiwan plus smaller islands nearby and off coast of China's Fujian Province;",
                "counties:", "Changhua, Chiayi, Hsinchu, Hualien,",
                "cities:", "Chiayi, Hsinchu, Keelung",
                "special municipalities:", "Kaohsiung (city), New Taipei (city), Taipei (city),",
                "note:", "Taiwan uses a variety of romanization systems;"]
    assert [*html_with_nested_paragraphs.stripped_strings] == expected


def test_soup_with_breaks(html_with_breaks):
    assert [*html_with_breaks.stripped_strings] == ['3.3% of GDP (2019) (approximately $2.35 billion)',
                                              '3.2% of GDP (2018) (approximately $2.31 billion)',
                                              '3.3% of GDP (2017) (approximately $2.34 billion)',
                                              '3.1% of GDP (2016) (approximately $2.6 billion)',
                                              '2.9% of GDP (2015) (approximately $2.22 billion)']


def test_iterating_through_tags(html_with_nested_paragraphs):
    for strong_tag in html_with_nested_paragraphs.find_all("strong", recursive=True):
        print(strong_tag)
        if strong_tag.next_element.next.strip():
            print(strong_tag.next.find_next("p"))
        else:
            print(strong_tag.next_element.next)
        # print(strong_tag.extract())
        # html_with_nested_paragraphs.extract(html_with_nested_paragraphs.index(strong_tag))
    print([*html_with_nested_paragraphs.stripped_strings])
