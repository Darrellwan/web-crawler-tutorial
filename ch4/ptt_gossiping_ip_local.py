import requests
import time
import json
import re
from bs4 import BeautifulSoup

PTT_URL = 'https://www.ptt.cc'


def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url : ' + resp.url)
        print('Invalid status_code : ' + str(resp.status_code))
        return None
    else:
        return resp.text


# def get_ip(dom):
#
#
# def get_country(ip):


def get_articles(dom, today):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    article_divs = soup.find_all("div", "r-ent")

    for article_div in article_divs:
        if article_div.find("div", "date").text.strip() == today:
            push_count = 0
            push_str = article_div.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)  # 轉換字串為數字
                except ValueError:
                    # 若轉換失敗，可能是'爆'或 'X1', 'X2', ...
                    # 若不是, 不做任何事，push_count 保持為 0
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if article_div.find('a'):
                href = article_div.find('a')['href']
                title = article_div.find('a').text.strip()
                author = article_div.find('div', 'author').text.strip()
                articles.append({
                    "href": href,
                    "title": title,
                    "push_count": push_count,
                    "author": author
                })
    return articles, prev_url


def get_ip(dom):
    ip_pattern = "來自: \d+\.\d+\.\d+\.\d+"
    ip_match = re.search(ip_pattern, dom)
    if ip_match:
        ip = ip_match.group(0).replace("來自: ", "")
        return ip
    else:
        return None


def get_country(ip):
    if ip:
        data = json.loads(requests.get('http://freegeoip.net/json/' + ip).text)
        country_name = data['country_name'] if data['country_name'] else None
        city_name = data['city'] if data['city'] else None
        if country_name and city_name:
            return country_name + ', ' + city_name
        elif country_name:
            return country_name
        else:
            return None
    return None


if __name__ == '__main__':
    test_mode = False
    print("取得今日文章列表")
    current_page = get_web_page(PTT_URL + '/bbs/Gossiping/index.html')
    index = 0
    if current_page:
        articles = []
        today = time.strftime('%m/%d').lstrip('0')
        current_articles, prev_url = get_articles(current_page, today)
        index += 1
        while current_articles:
            articles += current_articles
            if test_mode:
                break
            print("目前第 %d 次執行撈取文章" % index + '共 %d 篇文章' % len(articles))
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)
            index += 1
        print('共 %d 篇文章' % (len(articles)))

        country_dict = dict()
        articles_len = len(articles)
        ip_index = 1
        for article in articles[:10]:
            page = get_web_page(PTT_URL + article['href'])
            if page:
                ip = get_ip(page)
                print("(%4s/%4s) 查詢 IP : %s " % (str(ip_index), str(articles_len), ip))
                ip_index += 1
                country_city = get_country(ip)
                if country_city in country_dict.keys():
                    country_dict[country_city] += 1
                else:
                    country_dict[country_city] = 1

        print('各國 IP 分布')
        for k, v in country_dict.items():
            print(k, v)
