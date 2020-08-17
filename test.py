from app.scraper.akwam_scraper import *
import json
import time

url = 'https://eg4.akwam.net/movies?page='
data = scrape_all_series(baseUrl=url, num_pages=100)
with open('all_movies.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)