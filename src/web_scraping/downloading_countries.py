from src.global_vars import COUNTRIES_PATH
import csv


# Note that metric "geographic overview should be downloaded before all other metrics"
def get_all_countries():
    print("DOWNLOAD COUNTRIES")
    with open(COUNTRIES_PATH) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        world_countries = [row[0] for row in reader]
        world_countries.remove('South Africa')
        return sorted(list(set(world_countries)))
