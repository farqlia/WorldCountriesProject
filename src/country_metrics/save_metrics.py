import csv

from src.country_metrics.save_to_csv import parametrize_csv_saving
import src.web_scraping.destructuring_functions as destructuring
import src.web_scraping.conversion_functions as convert_values
from typing import List
from numpy import repeat, c_, array
from functools import partial
from src.global_vars import DATA_PATH, COUNTRIES_PATH

save_list_like = partial(parametrize_csv_saving,
                         destructure_method=destructuring.destructure_list_like)

save_ll_with_numbers = save_list_like(conversion_function=convert_values.convert_to_number)
save_ll_with_quantity = save_list_like(conversion_function=convert_values.convert_quantity_of)
save_ll_with_fraction = save_list_like(conversion_function=convert_values.convert_fraction)

save_text = partial(parametrize_csv_saving,
                    destructure_method=destructuring.destructure_text_paragraph)

save_txt_with_numbers = save_text(conversion_function=convert_values.convert_to_number)
save_txt_with_fraction = save_text(conversion_function=convert_values.convert_fraction)
save_txt_with_quantity = save_text(conversion_function=convert_values.convert_quantity_of)
save_txt_only_header = save_text(conversion_function=convert_values.extract_header)

save_nested_list_like = partial(parametrize_csv_saving,
                                destructure_method=destructuring.destructure_nested_lists)

save_nll_with_quantity = save_nested_list_like(conversion_function=convert_values.convert_quantity_of)


# This will be used to save country names
# The slight problem here is that some countries belong to more than one continent,
# so the index for dataframe might not be unique
def save_geographic_overview(country_samples):
    countries_on_continents = list(country_samples['World'])[9:15]
    with open(COUNTRIES_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'continent'])
        for p in countries_on_continents:
            continent, countries = convert_values.get_continent_and_countries(p)
            rows = c_[array(countries), repeat(continent, repeats=len(countries))]
            writer.writerows(list(rows))


def get_path(name):
    return DATA_PATH.joinpath(name + ".csv")


def save_infant_mortality_rate(country_samples):
    save_ll_with_numbers(get_path("infant_mortality_rate"),
                         ['total', 'male', 'female'],
                         country_samples)


def save_population_growth_rate(country_samples):
    save_txt_with_numbers(get_path("population_growth_rate"), ['rate'],
                          country_samples)


def save_age_structure(country_samples):
    save_ll_with_numbers(get_path("age_structure"),
                         ['0-14 years', '15-64 years', '65 years and over'],
                          country_samples)


def save_birth_rate(country_samples):
    save_txt_with_numbers(get_path("birth_rate"), ["rate"],
                          country_samples)


def save_net_migration_rate(country_samples):
    save_txt_with_fraction(get_path("net_migration_rate"), ['rate'],
                           country_samples)


def save_alcohol_consumption_per_capita(country_samples):
    save_ll_with_quantity(get_path("alcohol_consumption_per_capita"),
                          ["total", "beer", "wine", "spirits", "other alcohols"],
                          country_samples)


def save_child_marriage(country_samples):
    save_ll_with_numbers(get_path("child_marriage"),
                         ["women married by age 15", "women married by age 18", "men married by age 18"],
                         country_samples)


def save_contraceptive_prevalence_rate(country_samples):
    save_txt_with_numbers(get_path("contraceptive_prevalence_rate"),
                          ["rate"], country_samples)


def save_currently_married_women_ages_15_49(country_samples):
    save_txt_with_numbers(get_path("currently_married_women_ages_15_49"),
                          ['rate'], country_samples)


def save_death_rate(country_samples):
    save_txt_with_fraction(get_path("death_rate"),
                           ['rate'], country_samples)


def save_dependency_ratios(country_samples):
    save_ll_with_numbers(get_path("dependency_ratios"),
                           ['total dependency ratio', 'youth dependency ratio', 'elderly dependency ratio',
                            'potential support ratio'], country_samples)


def save_drinking_water_source(country_samples):
    save_nll_with_quantity(get_path("drinking_water_source"),
                           ["improved_urban", "improved_rural", "improved_total", "unimproved_urban",
                            "unimproved_rural", "unimproved_total"], country_samples)


def save_education_expenditures(country_samples):
    save_txt_with_quantity(get_path("education_expenditures"),
                           ["rate"], country_samples)

# Add food insecurity as a categorical variable


def save_gdp_official_exchange_rate(country_samples):
    save_txt_with_numbers(get_path("gdp_official_exchange_rate"),
                          ['rate'], country_samples)


def save_gini_index_coefficient_distribution_of_family_income(country_samples):
    save_txt_with_numbers(get_path("gini_index_coefficient_distribution_of_family_income"),
                          ['rate'], country_samples)


# How to get HIV.AIDS
# With this metric, if there is only industry and services available, then
# place it as industry
def save_labor_force_by_occupation(country_samples):
    save_ll_with_numbers(get_path("labor_force_by_occupation"),
                         ['agriculture', 'industry', 'services',
                          'industry and services'],
                         country_samples)


def save_life_expectancy_at_birth(country_samples):
    save_ll_with_numbers(get_path("life_expectancy_at_birth"),
                         ['total population', 'male', 'female'],
                         country_samples)


def save_literacy(country_samples):
    save_ll_with_numbers(get_path("literacy"),
                         ['total population', 'male', 'female'],
                         country_samples)


def save_maternal_mortality_ratio(country_samples):
    save_txt_with_fraction(get_path("maternal_mortality_ratio"),
                           ['rate'], country_samples)


def save_mothers_mean_age_at_first_birth(country_samples):
    save_txt_with_numbers(get_path("mothers_mean_age_at_first_birth"),
                          ['rate'], country_samples)


def save_obesity_adult_prevalence_rate(country_samples):
    save_txt_with_numbers(get_path("obesity_adult_prevalence_rate"),
                          ['rate'], country_samples)


def save_physicians_density(country_samples):
    save_txt_with_fraction(get_path("physicians_density"), ['rate'],
                           country_samples)


def save_population_below_poverty_line(country_samples):
    save_txt_with_numbers(get_path("population_below_poverty_line"),
                          ['rate'], country_samples)


def save_school_life_expectancy_primary_to_tertiary_education(country_samples):
    save_ll_with_numbers(get_path("school_life_expectancy_primary_to_tertiary_education"),
                         ["total", "male", "female"], country_samples)


def save_sex_ratio(country_samples):
    save_ll_with_fraction(get_path("sex_ratio"),
                          ["at birth", "0-14 years", "15-64 years", "65 years and over", "total population"],
                          country_samples)


def save_tobacco_use(country_samples):
    save_ll_with_numbers(get_path("tobacco_use"),
                         ["total", "male", "female"],
                         country_samples)


def save_total_fertility_rate(country_samples):
    save_txt_with_fraction(get_path("total_fertility_rate"),
                           ["fertility_rate"], country_samples, field_names=["fertility_rate"])


def save_unemployment_rate(country_samples):
    save_txt_with_numbers(get_path("unemployment_rate"),
                          ["2021"], country_samples, field_names=["2021"])


def save_current_health_expenditure(country_samples):
    save_txt_with_numbers(get_path("current_health_expenditure"),
                          ['expenditures'], country_samples, field_names=['expenditures'])


def save_median_age(country_samples):
    save_ll_with_numbers(get_path("median_age"),
                         ['total', 'male', 'female'], country_samples)


def save_location(country_samples):
    save_text(conversion_function=convert_values.extract_location)(get_path("location"),
                                                                   ['location'], country_samples, ['location'])


def save_food_insecurity(country_samples):
    save_txt_only_header(get_path("food_insecurity"),
                       ['food insecurity'], country_samples, field_names=['food insecurity'])


def save_population(country_samples):
    save_txt_with_numbers(get_path("population"),
                          ['population'], country_samples, field_names=['population'])
