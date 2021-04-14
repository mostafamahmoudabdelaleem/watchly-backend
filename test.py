from app.scraper.arabseed_scraper import *
import json
import time
import requests

sleep_time = 1 * 60 * 60

while True:
    movies = []
    start_time = time.time()

    movies = collect(category=FORIGN_MOVIES_CATEGORY)

    total_time = round(time.time() - start_time, 3)
    print("[ArabseedScraper]: Scraped <{0}> items in <{1}> second.".format(len(movies),total_time))

    with open('ramdan2021.json', 'w', encoding='utf-8') as outfile:
        json.dump(movies, outfile, indent=4, ensure_ascii=False)

    j = json.dumps(movies, separators=(',', ':'), ensure_ascii=False)

    update_url = 'https://api.watchly.msoft.ml/api/ramdan'
    #update_url = 'http://localhost:5000/api/ramdan'

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    resp = requests.post(
        update_url, 
        data=j.encode('utf-8'), 
        headers=headers
    )
    print('[ArabseedScraper]: Data sent to backend with status code = {0}'.format(resp.status_code))
    print('[ArabseedScraper]: Sleeping for 1 Hours')
    time.sleep(sleep_time)