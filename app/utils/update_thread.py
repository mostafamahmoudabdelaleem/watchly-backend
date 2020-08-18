import time
import json
import threading
from app.scraper.akwam_scraper import scrape_all_series


DEFAULT_URL = 'https://eg4.akwam.net/{0}?page='
DEFAULT_UPDATE_INTERVAL = 6 * 60 * 60 * 1000 # Every 6 hours
DEFAULT_NUM_PAGES = 100

UPDATE_THREAD_NAME = 'Update-Thread'
MOVIES_URL = DEFAULT_URL.format('movies')
SERIES_URL = DEFAULT_URL.format('series')
MOVIES_FILENAME = 'all_movies.json'
SERIES_FILENAME = 'all_series.json'


def update_function(url, filename):
    data = scrape_all_series(baseUrl=url, num_pages=DEFAULT_NUM_PAGES)
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    del(data)
    return True


def thread_target(update_interval):
    print('[{0}]: has started successfully.'.format(UPDATE_THREAD_NAME))
    condition = False

    while(true):
        condition = update_function(MOVIES_URL, MOVIES_FILENAME)
        if(condition):
            print('[{0}]: Movies list updated successfully.'.format(UPDATE_THREAD_NAME))
        else:
            print('[{0}]: Failed while updating movies list.'.format(UPDATE_THREAD_NAME))

        condition = update_function(SERIES_URL, SERIES_FILENAME)
        if(condition):
            print('[{0}]: Series list updated successfully.'.format(UPDATE_THREAD_NAME))
        else:
            print('[{0}]: Failed while updating series list.'.format(UPDATE_THREAD_NAME))

        time.sleep(update_interval)


def start_update_thread(update_interval=DEFAULT_UPDATE_INTERVAL):
    threading.Thread(
        target=thread_target, 
        args=(update_interval,),
        name=UPDATE_THREAD_NAME
        ).start()

