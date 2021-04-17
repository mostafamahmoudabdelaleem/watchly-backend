'''
Implementaion of Arabseed scraper here 

don't change this function name of first parameter
keyword is word to scrape data about it.
you can add more params as you wish but specify their default values
'''

import os
import re
import time
import requests
import threading
from bs4 import BeautifulSoup
import hashlib

ARABSEED_BASE_URL = 'https://arabseed.onl'
FORIGN_MOVIES_CATEGORY = 'category/مسلسلات-رمضان-2021'
FORIGN_SERIES_CATEGORY = 'category/foreign-series'

HOME_PAGE_SINGLE_ITEM_CLASS = 'MovieBlock'

MOVIE_POSTER_CLASS = 'Poster'
MOVIE_PLOT_CLASS = 'StoryLine'
MOVIE_TITLE_CLASS = 'TitleArea'
MOVIE_TAX_CLASS = 'MetaTermsInfo'

MOVIE_DOWNLOAD_ITEMS_CLASS = 'ArabSeedServer'

def get_headers(url): 
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate', 
        'Accept': '*/*', 
        'Connection': 'keep-alive'
        ''
    }


def scrape_main_page(url):
    data = []
    html = requests.get(url)
    if (html.status_code != 200):
        print(print('[ArabseedScraper]: Request for <{}> returned <{}>'.format(url, html.status_code)))
    soup = BeautifulSoup(html.text, 'lxml')
    movies_divs = soup.find_all('div', {'class': HOME_PAGE_SINGLE_ITEM_CLASS})
    print('[ArabseedScraper]: Found <{}> item in url <{}>'.format(len(movies_divs), url))

    for div in movies_divs:
        movie = {}
        m_link = div.find('a')['href']
        movie['id'] = hashlib.sha256("{0}".format(m_link).encode('utf-8')).hexdigest()
        movie['link'] = m_link
        movie['name'] = div.find('a').find('div', {'class': 'BlockName'}).find('h4').string
        rating_em = div.find('div', {'class': 'number'})
        if rating_em == None:
            movie['rating'] = ''
        else:
            movie['rating'] = rating_em.find('span').text
        
        data.append(movie)
    
    return data


def get_movie_img(soup):
    img_div = soup.find('div', {'class': MOVIE_POSTER_CLASS})
    img_tag = img_div.find('img')
    return img_tag['data-image']

def get_movie_plot(soup):
    plot_div = soup.find('div', {'class': MOVIE_PLOT_CLASS})
    plot_tag = plot_div.find('p')
    return plot_tag.string

def get_movie_taxs(soup):
    tax_div = soup.find('div', {'class': MOVIE_TAX_CLASS})
    taxs = tax_div.find_all('li')

    quality = ''
    year = ''
    duration = ''
    for tax in taxs:
        if tax.find('span').string == 'الجودة : ':
            quality = (tax.find('a').string)
        if tax.find('span').string == 'تاريخ الاصدار : ':
            year = (tax.find('a').string)
        if tax.find('span').string == 'مدة العرض : ':
            duration = (tax.find('a').string)
    return {
        'quality': quality,
        'year': year,
        'duration': duration
    }

def get_movie_sources(link):
    data = {}
    url = link + 'download/'
    html = requests.get(url)
    if (html.status_code != 200):
        print(print('[ArabseedScraper]: Request for <{}> returned <{}>'.format(url, html.status_code)))
    soup = BeautifulSoup(html.text, 'lxml')

    a_tags = soup.find_all('a', {'class': MOVIE_DOWNLOAD_ITEMS_CLASS})
    for tag in a_tags:
        tag_name = tag.find('span').string
        #if tag_name == 'Arabseed مباشر' or tag_name == 'Arabseed':
        data[tag.find('p').string] = tag['href']
            
    return data

def scrape_movie(url):
    data = {}
    html = requests.get(url)
    if (html.status_code != 200):
        print(print('[ArabseedScraper]: Request for <{}> returned <{}>'.format(url, html.status_code)))
    soup = BeautifulSoup(html.text, 'lxml')
    
    tax = get_movie_taxs(soup)
    sources = get_movie_sources(url)

    data['img_link'] = get_movie_img(soup)
    data['plot'] = get_movie_plot(soup)
    data['quality'] = tax['quality']
    data['year'] = '2021' #tax['year']
    data['duration'] = tax['duration']
    data['sources_links'] = sources

    return data

def merge_dict(old, new):
    return {
        "id": old['id'],
        "link": old['link'],
        "rating": old['rating'],
        'name': old['name'],
        'img_link': new['img_link'],
        'plot': new['plot'],
        'quality': new['quality'],
        'year': new['year'],
        'duration': new['duration'],
        'sources_links': new['sources_links']
    }

def collect(start = 1, end = 2, category = FORIGN_MOVIES_CATEGORY):
    global_movies = []
    movies_data = []

    for i in range(start, end):
        page_url = "{0}/{1}/?page={2}".format(ARABSEED_BASE_URL, category, (i))
        movies_data += scrape_main_page(page_url)
        #print(page_url)

    #parts = partition(movies_data)
    parts = [movies_data]
    start_threads_job(parts, scrape_thread_callback, global_movies)
    
    return global_movies

def partition(arr, num_threads = 4):
    parts = []
    r = len(arr) / num_threads # r represent ratio between part size for each thread
    for i in range(num_threads):
        st = int(i*r)
        ed = int((i+1)*r)
        part = arr[st:ed]
        parts.append(part)
    return parts

def start_threads_job(threads_part_array, callback, global_result_array):
    threads = []
    c=1
    #print('Collectin Threads Num => {0}'.format(len(threads_part_array)))
    for part in threads_part_array:
        part_id = "id_{0}".format(c)
        thread = threading.Thread(target=callback, args=(part, global_result_array), name=part_id)
        thread.start()
        threads.append(thread)
        c += 1
    
    for thread in threads:
        thread.join()

def scrape_thread_callback(parts_array, global_array):
    for data in parts_array:
        movie = scrape_movie(data['link'])
        global_array.append(merge_dict(data, movie))

