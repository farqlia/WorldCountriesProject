from src.web_scraping.downloading import download_metrics, assert_all_are_downloaded

metrics = ['infant mortality rate', 'population growth rate',
            'age structure', 'birth rate', 'net migration rate',
            'alcohol consumption per capita', 'child marriage',
           'contraceptive prevalence rate', 'currently married women ages 15 49',
           'death rate', 'education expenditures',
           'gdp_official_exchange_rate', 'gini_index_coefficient_distribution_of_family_income',
           'labor_force_by_occupation', 'life_expectancy_at_birth',
           'literacy', 'maternal_mortality_ratio',
           'mothers_mean_age_at_first_birth', 'obesity_adult_prevalence_rate',
           'physicians_density', 'population_below_poverty_line',
           'school_life_expectancy_primary_to_tertiary_education',
           'sex_ratio', 'tobacco_use', 'total_fertility_rate',
           'unemployment_rate'

           ]

metrics = [
    'infant mortality rate', 'population growth rate',
    'age structure', 'birth rate', 'net migration rate',
    'alcohol consumption per capita', 'child marriage',
    'contraceptive prevalence rate',
    'currently married women ages 15 49', 'death rate',
    'education expenditures', 'gdp official exchange rate',
    'gini index coefficient distribution of family income',
    'labor force by occupation', 'life expectancy at birth',
    'literacy', 'maternal mortality ratio',
    'mothers mean age at first birth',
    'obesity adult prevalence rate', 'physicians density',
    'population below poverty line',
    'school life expectancy primary to tertiary education',
    'sex ratio', 'tobacco use', 'total fertility rate',
    'unemployment rate', 'current health expenditure'
]

# TODO: solve with 'drinking water source'
# download_metrics([m.replace('_', ' ') for m in metrics])
download_metrics(['current health expenditure'])
print("[")
print(", ".join("'" + m.replace('_', ' ') + "'" for m in metrics))
print("]")
# assert_all_are_downloaded(metrics)

print("done")