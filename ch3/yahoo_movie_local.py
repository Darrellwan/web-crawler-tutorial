import sys

import requests
import re
import json
from bs4 import BeautifulSoup

Y_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'

# 以下網址後面加上 "/id=MOVIE_ID" 即為該影片各項資訊
Y_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
Y_PHOTO_URL = 'https://tw.movies.yahoo.com/movieinfo_photos.html'  # 劇照
Y_TIME_URL = 'https://tw.movies.yahoo.com/movietime_result.html'  # 時刻表


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Invalid url ", resp.url)
        print("Invalid status_code ", resp.status_code)
        return None
    else:
        return resp.text


def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'release_info_text')
    for row in rows:
        # dict means key is unique
        movie = dict()
        movie['expectation'] = row.find('div', 'leveltext').span.text.strip()
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        movie['eng_name'] = row.find('div', 'en').a.text.strip()
        movie['eng_name'] = row.find('div', 'en').a.text.strip()
        movie['movie_id'] = get_movie_id(row.find('div', 'release_movie_name').a['href'])
        movie['poster_url'] = row.parent.find_previous_sibling('div', 'release_foto').a.img['src']
        movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        movie['intro'] = row.find('div', 'release_text').text.replace(u'詳全文', '').strip()
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs.keys() else ''
        movies.append(movie)
        print(movie['ch_name'])
        print("詳細內容介紹")
        get_complete_intro(movie['movie_id'])

    return movies


def get_date(date_str):
    # e.g. "上映日期：2017-03-23" -> match.group(0): "2017-03-23"
    date_pattern = '\d+-\d+-\d'
    date_match = re.search(date_pattern, date_str)
    if date_match is None:
        return date_str
    else:
        return date_match.group(0)


def get_movie_id(url):
    #      -> match.group(0): "/id=6707"
    id_pattern = '/id=\d+'
    id_match = re.search(id_pattern, url)
    if id_match is None:
        return url
    else:
        return id_match.group(0).replace('/id=', '')


def get_complete_intro(movie_id):
    # https://movies.yahoo.com.tw/movieinfo_main.html/id={movie_id}
    movie_url = Y_INTRO_URL + '/id=' + movie_id
    movie_resp = get_web_page(movie_url)
    movie_soup = BeautifulSoup(movie_resp, 'html5lib')
    intro_div = movie_soup.find('div', 'gray_infobox_inner')
    intro_span = intro_div.find('span', 'title2')
    if intro_span:
        print(intro_span['title2'])
    else:
        print(intro_div.text.strip())
    return None


def main():
    page = get_web_page(Y_MOVIE_URL)
    if page:
        movies = get_movies(page)
        for movie in movies:
            print(movie)
        with open('movie.json', 'w', encoding='UTF-8') as f:
            json.dump(movies, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    main()
