from arabseed_scraper import collect, FORIGN_MOVIES_CATEGORY
import json
import time
import requests

def cron_job():
    start_time = time.time()
    movies = collect(category=FORIGN_MOVIES_CATEGORY)
    total_time = round(time.time() - start_time, 3)
    print("[ArabseedScraper]: Scraped <{0}> items in <{1}> second.".format(len(movies),total_time))

    if (len(movies) < 1):
        print('[ArabseedScraper]: No data scraped')
        return

    j = json.dumps(movies, separators=(',', ':'), ensure_ascii=False)
    resp = requests.post(
        'https://api.watchly.msoft.ml/api/ramdan', 
        data=j.encode('utf-8'), 
        headers={
            'Content-Type': 'application/json; charset=utf-8'
        }
    )
    print('[ArabseedScraper]: Data sent to backend with status code = {0}'.format(resp.status_code))


if __name__ == "__main__":
    while True:
        cron_job()
        print('[ArabseedScraper]: Sleeping for 2 hour')
        time.sleep(2 * 60 * 60)