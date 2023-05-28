import src.web_scraping.downloading_metrics as downloading
import pandas as pd
from src.global_vars import DATA_PATH
import numpy as np
from scipy.stats import pearsonr, spearmanr



def assign_continents():
    geographic_overview = pd.read_csv(DATA_PATH / 'geographic_overview.csv')

    duplicate_countries = {'Azerbaijan': 'Asia', 'Georgia': 'Asia',
                           'Kazakhstan': 'Asia',
                            'Russia': 'Europe', 'Turkey': 'Asia'}

    geographic_overview = geographic_overview.drop_duplicates(subset=['country'], keep='first')
    geographic_overview.at[geographic_overview[geographic_overview['country'] == 'Czech Republic'].index[0], 'country'] = 'Czechia'
    geographic_overview = geographic_overview.set_index(keys='country')
    for key, value in duplicate_countries.items():
        geographic_overview.at[key] = value

    return geographic_overview


def get_location_df():

    location = downloading.open_metric('location')

    missing_regions = {
        'El Salvador': 'South America',
        'France': 'Europe',
        'Seychelles': 'Africa'
    }

    for key, value in missing_regions.items():
        location.at[key] = value

    assert sum(location.isna().values) == 0
    return location


def merge_metrics(index):
    infant_mortality_rate = downloading.open_metric('infant mortality rate')
    population_growth_rate = downloading.open_metric('population growth rate')
    birth_rate = downloading.open_metric('birth rate')
    net_migration_rate = downloading.open_metric('net migration rate')
    alcohol_consumption_per_capita = downloading.open_metric('alcohol consumption per capita')
    child_marriage = downloading.open_metric('child marriage')
    life_expectancy = downloading.open_metric('life expectancy at birth')
    death_rate = downloading.open_metric('death rate')
    contraceptive_prevalence = downloading.open_metric('contraceptive prevalence rate')
    currently_married_women_ages_15_49 = downloading.open_metric('currently married women ages 15 49')
    maternal_mortality_ratio = downloading.open_metric('maternal mortality ratio')
    health_expenditures = downloading.open_metric('current health expenditure')
    gdp = downloading.open_metric('gdp official exchange rate')
    gini_index_coefficient_distribution_of_family_income = downloading.open_metric(
        'gini index coefficient distribution of family income')
    labor_force_by_occupation = downloading.open_metric('labor force by occupation')
    literacy = downloading.open_metric('literacy')
    education_expenditures = downloading.open_metric('education expenditures')
    population_below_poverty = downloading.open_metric('population below poverty line')
    fertility_rate = downloading.open_metric('total fertility rate')
    mothers_mean_age_at_first_birth = downloading.open_metric('mothers mean age at first birth')
    # This could be split for age-groups
    sex_ratio = downloading.open_metric('sex ratio')
    obesity_adult_prevalence_rate = downloading.open_metric('obesity adult prevalence rate')
    physicians_density = downloading.open_metric('physicians density')
    school_life_expectancy = downloading.open_metric('school life expectancy primary to tertiary education')
    tobacco_use = downloading.open_metric('tobacco use')
    unemployment_rate = downloading.open_metric('unemployment rate')
    # This rather not
    dependency_ratios = downloading.open_metric('dependency ratios')
    drinking_water_source = downloading.open_metric('drinking water source')
    population = downloading.open_metric('population')
    budget_surplus_or_deficit = downloading.open_metric('budget surplus or deficit')
    energy_consumption = downloading.open_metric('energy consumption per capita')
    gdp_components = downloading.open_metric('gdp composition by end use')
    industrial_production_rate = downloading.open_metric('industrial production growth rate')
    taxes_and_other_revenues = downloading.open_metric('taxes and other revenues')
    internet_users = downloading.open_metric('internet users')

    countries_data = pd.DataFrame(index=index)

    countries_data['infant mortality rate'] = infant_mortality_rate['total']
    countries_data['population growth rate'] = population_growth_rate['rate']
    countries_data['net migration rate'] = net_migration_rate['rate']
    countries_data['alcohol consumption per capita'] = alcohol_consumption_per_capita['total']
    countries_data['wine consumption'] = alcohol_consumption_per_capita['wine']
    countries_data['women marriage by 18'] = child_marriage['women married by age 18']
    countries_data['men marriage by 18'] = child_marriage['men married by age 18']
    countries_data['currently married women ages 15-49'] = currently_married_women_ages_15_49['rate']
    countries_data['birth rate'] = birth_rate['rate']
    countries_data['life expectancy female'] = life_expectancy['female']
    countries_data['life expectancy male'] = life_expectancy['male']
    countries_data['life expectancy total'] = life_expectancy['total population']
    countries_data['death rate'] = death_rate['rate']
    countries_data['gini index coefficient distribution of family income'] = \
    gini_index_coefficient_distribution_of_family_income['rate']
    labor_force_by_occupation.at['Togo', 'agriculture'] /= 100
    labor_force_by_occupation.at['Togo', 'services'] /= 100
    countries_data['agriculture occupation ratio'] = labor_force_by_occupation['agriculture']
    countries_data['industry occupation ratio'] = pd.DataFrame(
        data=np.where(np.isnan(labor_force_by_occupation['industry']),
                      labor_force_by_occupation['industry and services'], labor_force_by_occupation['industry']),
        index=labor_force_by_occupation.index)
    countries_data['services occupation ratio'] = labor_force_by_occupation['services']
    countries_data['contraceptive prevalence'] = contraceptive_prevalence['rate']
    countries_data['maternal mortality ratio'] = maternal_mortality_ratio['rate']
    countries_data['health expenditures'] = health_expenditures['expenditures']
    countries_data['gdp'] = gdp['rate']
    countries_data['literacy female'] = literacy['female']
    countries_data['literacy male'] = literacy['male']
    countries_data['literacy total'] = literacy['total population']
    countries_data['mothers mean age at first birth'] = mothers_mean_age_at_first_birth['rate']
    countries_data['obesity adult prevalence rate'] = obesity_adult_prevalence_rate['rate']
    countries_data['physicians density'] = physicians_density['rate']
    countries_data['school life expectancy female'] = school_life_expectancy['female']
    countries_data['school life expectancy male'] = school_life_expectancy['male']
    countries_data['school life expectancy total'] = school_life_expectancy['total']
    countries_data['tobacco use female'] = tobacco_use['female']
    countries_data['tobacco use male'] = tobacco_use['male']
    countries_data['tobacco use total'] = tobacco_use['total']
    countries_data['education expenditures'] = education_expenditures['rate']
    countries_data['population below poverty'] = population_below_poverty['rate']
    countries_data['fertility rate'] = fertility_rate['fertility_rate']
    countries_data['drinking water source improved'] = drinking_water_source['improved_total']
    countries_data['drinking water source unimproved'] = drinking_water_source['unimproved_total']
    countries_data['sex ratio'] = sex_ratio['total population']
    countries_data['unemployment rate'] = unemployment_rate['2021']
    countries_data['population'] = population['population']
    countries_data['budget +/- perc of GDP'] = budget_surplus_or_deficit['percentage of GDP']
    countries_data['energy consumption per person'] = energy_consumption['consumption per person']
    countries_data['gdp household consumption'] = gdp_components['household consumption']
    countries_data['gdp government consumption'] = gdp_components['government consumption']
    countries_data['gdp exports of goods and services'] = gdp_components['exports of goods and services']
    countries_data['gdp imports of goods and services'] = gdp_components['imports of goods and services']
    countries_data['industrial production growth rate'] = industrial_production_rate['rate']
    countries_data['taxes and other revenues'] = taxes_and_other_revenues['rate']
    countries_data['internet users'] = internet_users['percent of population']

    return countries_data


# Returns tuple of metric result and type
# Checks for pearson correlation, spearmanr, logarythmic
# Only its upper left triangle is filled
def compute_dependency_matrix(country_metrics, dependency_fun):
    n = len(country_metrics.columns)
    matrix = np.zeros(shape=(n, n))
    for i in range(n):
        for j in range(i, n):
            matrix[i, j] = dependency_fun(country_metrics.iloc[:, i], country_metrics.iloc[:, j])[0]

    return matrix


# Returns dropped columns
def drop_columns_with_percent_of_nulls(country_metrics, percentage=0.5):
    n_countries = len(country_metrics)
    null_counts_per_metric = country_metrics.isna().sum(axis=0).sort_values()
    columns_to_drop = null_counts_per_metric[null_counts_per_metric / n_countries > percentage].index
    country_metrics.drop(columns_to_drop, inplace=True, axis=1)
    return columns_to_drop



if __name__ == "__main__":
    print(get_location_df())
    countries_data = merge_metrics()