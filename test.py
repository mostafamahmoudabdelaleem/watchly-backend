#from app.scraper.akwam_scraper import *
from app.scraper.arabseed_scraper import *
import json
import time
import math
import requests
import sys


def start_threads_job_2(st, ed, num_thread, callback, global_array):
    threads = []
    part_size = math.ceil(ed/num_thread)
    ed += 1

    for i in range(st, ed, part_size):
        part_id = "id_{0}".format(i)
        start = i
        end = i+part_size
        if end > ed:
            end = ed
        thread = threading.Thread(target=callback, args=(start, end, global_array), name=part_id)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def scrape_thread_callback_2(st, ed, global_array):
    print("[ArabseedScraper]: Collecting From Page<{0}> to <{1}>".format(st,ed-1))
    local_movies = collect_movies(st, ed)
    global_array += local_movies

count = 0
movies = []
start_time = time.time()

#start_threads_job_2(1, 10, 5, scrape_thread_callback_2, movies)
movies = collect(end=3, category=FORIGN_SERIES_CATEGORY)

total_time = round(time.time() - start_time, 3)
print("[ArabseedScraper]: Scraped <{0}> items in <{1}> second.".format(len(movies),total_time))


j = json.dumps(movies, separators=(',', ':'), ensure_ascii=False)
print(sys.getsizeof(j.encode('utf-8')))



headers = {
    'Content-Type': 'application/json; charset=utf-8'
}
resp = requests.post(
    'https://api.watchly.msoft.ml/api/series', 
    data=j.encode('utf-8'), 
    headers=headers
)
print(resp.status_code)