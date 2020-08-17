'''
Implementaion of Akwam scraper here 

don't change this function name of first parameter
keyword is word to scrape data about it.
you can add more params as you wish but specify their default values
'''
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache

AKWAM_BASE_URL = 'https://eg4.akwam.net/series?section=29&year=2020&language=1&page='

HOME_PAGE_SINGLE_ITEM_CLASS = 'col-lg-auto col-md-4 col-6 mb-12'
HOME_PAGE_SINGLE_ITEM_LINK_CLASS = 'box'
HOME_PAGE_SINGLE_ITEM_RATING_CLASS = 'label rating'
HOME_PAGE_SINGLE_ITEM_QUALITY_CLASS = 'label quality'
HOME_PAGE_SINGLE_ITEM_NUM_EP_CLASS = 'label series'
HOME_PAGE_SINGLE_ITEM_IMG_CLASS = 'img-fluid w-100 lazy'

EPISODE_DOWNLOAD_SHORT_LINK_CLASS = 'link-btn link-download d-flex align-items-center px-3'
SHORTLINK_PAGE_DOWNLOAD_LINK_CLASS = 'download-link'
DOWNLOAD_PAGE_LINK_CLASS = 'font-size-16 text-muted'

EPISODE_ITEM_CLASS = 'bg-primary2 p-4 col-lg-4 col-md-6 col-12'
EPISODE_TITLE_LINK_CLASS = 'text-white'
EPISODE_DATE_CLASS = 'entry-date font-size-12 text-muted mb-2'
EPISODE_THUMBNAIL_CLASS = 'img-fluid'

CACHE_TTL = os.getenv("CACHE_TTL", "1")
CACHE_SIZE = os.getenv("CACHE_SIZE", "1")

TTL = int(CACHE_TTL) * 3600
SIZE = int(CACHE_SIZE) * 1024


@cached(cache=TTLCache(maxsize=1024, ttl=(3600*24)))
def scrape_all_series(baseUrl= AKWAM_BASE_URL,num_pages=3):
    start_time = time.time()
    data = []

    for i in range(num_pages):
        url = baseUrl + str(i+1)
        data += scrape_home_page(url)
    
    total_time = round(time.time() - start_time, 3)
    print("[AkwamScraper]: Scraped <{0}> series from <{1}> page in {2} second.".format(
        len(data), 
        num_pages, 
        total_time)
        )
    return data
 

@cached(cache=TTLCache(maxsize=SIZE, ttl=TTL))
def scrape_home_page(url):
    data = []
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    result = soup.find_all('div', {'class': HOME_PAGE_SINGLE_ITEM_CLASS})

    for val in result:
        link_tag = val.find('a', {'class': HOME_PAGE_SINGLE_ITEM_LINK_CLASS})
        img_tag = val.find('img', {'class': HOME_PAGE_SINGLE_ITEM_IMG_CLASS})
        rating_tag = val.find('span', {'class': HOME_PAGE_SINGLE_ITEM_RATING_CLASS})
        quality_tag = val.find('span', {'class': HOME_PAGE_SINGLE_ITEM_QUALITY_CLASS})

        if link_tag != None:
            link = link_tag['href']
        else:
            link = "None"

        if img_tag != None:
            img_link = img_tag['data-src']
        else:
            img_link = "None"
        
        if img_tag != None:
            name = img_tag['alt']
        else:
            name = "None"
        
        if rating_tag != None:
            rating = remove_html_tags(rating_tag)
        else:
            rating = "None"
        
        if quality_tag != None:
            quality = quality_tag.string
        else:
            quality = "None"
        
        r = {
            'name': name,
            'img_link': img_link,
            'link': link,
            'rating': rating,
            'quality': quality
        }
        data.append(r)

    return data


#@cached(cache=TTLCache(maxsize=SIZE, ttl=TTL))
def scrape_single_series(series_link):
    st = time.time()
    data = []
    html = requests.get(series_link)
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, 'lxml')
    result = soup.find_all('div', {'class': EPISODE_ITEM_CLASS})
    for val in result:
        title_link_tag = val.find('a', {'class': EPISODE_TITLE_LINK_CLASS})
        date_tag = val.find('p', {'class': EPISODE_DATE_CLASS})
        thumbnail_tag = val.find('img', {'class': EPISODE_THUMBNAIL_CLASS})

        if title_link_tag != None:
            title = title_link_tag.string
            link = title_link_tag['href']
        else:
            title = "None"
            link = "None"

        if date_tag != None:
            date = date_tag.string
        else:
            date = "None"

        if thumbnail_tag != None:
            thumbnail = thumbnail_tag['src']
            thumbnail = thumbnail.replace("thumb/320x190/", "")
        else:
            thumbnail = "None"

        r = {
            "title": title,
            "link": link,
            "date": date,
            "thumbnail": thumbnail
        }
        data.append(r)
    ed = time.time() - st
    print("[AkwamScraper]: Scraped series <{}> in {} Seconds.".format(series_link, round(ed,3)))

    return data


@cached(cache=TTLCache(maxsize=SIZE, ttl=TTL))
def scrape_links(link):
    st = time.time()
    links = []
    short_link = []
    download_page = []
    html = requests.get(link)
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, 'lxml')
    result = soup.find_all('a', {'class': EPISODE_DOWNLOAD_SHORT_LINK_CLASS})

    for val in result:
        short_link.append(val['href'])
    
    for url in short_link:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find('a', {'class': SHORTLINK_PAGE_DOWNLOAD_LINK_CLASS})
        download_page.append(result['href'])

    for url in download_page:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find('a', {'class': DOWNLOAD_PAGE_LINK_CLASS})
        links.append(result['href'])
    if len(links) > 2:
        r = {
            "1080p": links[0],
            "720p": links[1],
            "480p": links[2]
        }
    elif len(links) > 1:
        r = {
            "720p": links[0],
            "480p": links[1]
        }
    else:
        r = {
            "720p": links[0],
        }
    ed = time.time() - st
    print("[AkwamScraper]: Scraped episode <{}> in {} Seconds.".format(link, round(ed,3)))

    return r


def remove_html_tags(tag):
    return re.sub(r'<.*?>', '', str(tag))


