import pytest

from src.web_scraping.string_formatter import StringFormatter
import src.web_scraping.string_formatter as string_formatter


@pytest.fixture()
def builder():
    return StringFormatter.from_base("https://www.cia.gov/the-world-factbook")


def test_for_validate_pattern():
    string = "/field/{field}/another_field/{another_field}"
    assert string_formatter.VALIDATE_PATTERN.findall(string) == ['field', 'another_field']


class TestAppend:

    def test_for_append_string(self, builder):
        field_query = builder.append("field/{field}")
        assert field_query.string == "https://www.cia.gov/the-world-factbook/field/{field}"
        assert field_query != builder

    def test_for_append_same_parameter_twice(self, builder):
        field_query = builder.append("field/{field}")
        repeated_field_query = field_query.append("another_field/{another_field}")
        assert repeated_field_query.string == \
               "https://www.cia.gov/the-world-factbook/field/{field}/another_field/{another_field}"
        assert repeated_field_query.params == ['field', 'another_field']

    def test_for_valid_field_query(self, builder):
        field_query = builder.append("field/{field}")
        result = field_query.put_params(field="climate")
        assert field_query.params == ['field']
        assert result == "https://www.cia.gov/the-world-factbook/field/climate"

    def test_for_differing_keyword_name(self, builder):
        field_query = builder.append("a_field/{field}")
        assert field_query.string == 'https://www.cia.gov/the-world-factbook/a_field/{field}'
        with pytest.raises(ValueError):
            assert not field_query.put_params(field="population")

    def test_for_missing_field_query(self, builder):
        field_query = builder.append("field/{field}")
        with pytest.raises(ValueError):
            field_query.put_params(key="climate")