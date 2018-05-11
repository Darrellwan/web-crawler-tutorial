import re
from itertools import filterfalse

import requests
import time
import json
import sys
from bs4 import BeautifulSoup

PTT_URL = 'https://www.ptt.cc'


def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url : ', resp.url)
        print('Invalid response code : ', resp.status_code)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for div in divs:
        if div.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = div.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == "爆":
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if div.find('a'):
                href = div.find('a')['href']
                title = div.find('a').text
                author = div.find('div', 'author').text.strip()
                articles.append({
                    'title': title,
                    'author': author,
                    'href': PTT_URL+href,
                    'date': date,
                    'push_count': push_count
                })
    return articles, prev_url


def get_author_ids(posts, pattern):
    ids = set()
    for post in posts:
        if pattern in post['author']:
            ids.add(post['author'])
    return ids


def hot_filter(count, threshold):
    return count > threshold


def get_json_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as reader:
        gossiping_json = json.loads(reader.read())
    return gossiping_json


if __name__ == '__main__':
    current_page = get_web_page(PTT_URL + '/bbs/Gossiping/index.html')
    if (current_page):
        articles = []
        today = time.strftime("%m/%d").lstrip('0')
        current_articles, prev_url = get_articles(current_page, today)
        while current_articles:
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)

        print("今天有", len(articles), "篇文章")
        threshold = 50
        print("熱門文章(> %d 推) : " % (threshold))
        for article in articles[:]:
            if int(article['push_count']) > threshold:
                print(article)

        articles[:] = [article for article in articles if hot_filter(article['push_count'], threshold)]

        today_date = time.strftime("%y-%m-%d")
        file_name = 'gossiping_hot_'+today_date+'.json'
        with open(file_name, 'w', encoding='UTF-8') as fopen:
            json.dump(articles, fopen, indent=2, sort_keys=True, ensure_ascii=False)

    json_articles = get_json_content(file_name)
    ids_5566 = get_author_ids(json_articles, '5566')
    print("there are ", len(ids_5566), " person id with 5566")
    sys.exit(0)
