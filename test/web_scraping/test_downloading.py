from src.web_scraping.save_countries import save_countries, get_all_countries


def test_save_countries():
    save_countries()
    for country in get_all_countries():
        print(country)