from numpy import repeat, array, c_

from src.global_vars import COUNTRIES_PATH, DATA_PATH
import csv


def save_countries():
    with open(COUNTRIES_PATH, newline='', mode='w') as f_cnames:
        with open(DATA_PATH / "geographic_overview.csv") as f_geo_over:
            csv_reader = csv.DictReader(f_geo_over)
            csv_writer = csv.writer(f_cnames)
            csv_writer.writerow(["country"])
            countries = set()
            for row in csv_reader:
                countries.add(row['country'])

            countries.remove('Czech Republic')
            countries.remove('South Africa')
            countries.add('Czechia')
            for country in sorted(countries):
                csv_writer.writerow([country])


# Note that metric "geographic overview" should be downloaded before all other metrics
def get_all_countries():
    with open(COUNTRIES_PATH) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        world_countries = [row[0] for row in reader]
        return world_countries
