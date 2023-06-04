from src.web_scraping.downloading_metrics import download_metrics
from src.web_scraping.save_countries import save_countries

print("Download geographic overview")
download_metrics(['geographic overview'])
print("Done")
save_countries()
