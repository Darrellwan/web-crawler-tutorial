import requests
import re
from bs4 import BeautifulSoup


def main():
    homework1()
    homework2()
    homework3()
    homework4()


def homework1():
    resp_blog = requests.get('http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html')
    soup_blog = BeautifulSoup(resp_blog.text, 'html.parser')
    # part1
    blogs = soup_blog.find_all('div', 'card-blog')
    blog_length = len(blogs)
    print("there are " + str(blog_length) + " blog")


def homework2():
    # part2
    # find how many image's src contain string 'crawler'
    resp_blog = requests.get('http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html')
    soup_blog = BeautifulSoup(resp_blog.text, 'html.parser')
    img_len = len(soup_blog.find_all('img', {'src': re.compile('crawler')}))
    print("there are " + str(img_len) + " image's src contain crawler")


def homework3():
    # part 3
    # find how many lectures
    resp_table = requests.get('http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html')
    soup_table = BeautifulSoup(resp_table.text, 'html.parser')
    tbody_trs = soup_table.find('table', class_='table').find('tbody').find_all('tr')
    lecture_names = []
    for tbody_tr in tbody_trs:
        lecture_name = tbody_tr.find_all('td')[0].text
        if lecture_name not in lecture_names:
            lecture_names.append(lecture_name)
    print("there are " + str(len(lecture_names)) + " lectures")


def homework4():
    # part 4
    # find Dcard's 10 most popular articles name
    resp_dcard = requests.get('https://www.dcard.tw/f')
    soup_dcard = BeautifulSoup(resp_dcard.text, 'html.parser')

    popular_articles_divs = soup_dcard.find_all("div", class_="PostList_entry_1rq5L")
    print("dcard hot articles")
    for index, popular_articles_div in enumerate(popular_articles_divs):
        if index == 10:
            break
        popular_articles_title = popular_articles_div.find("h3").text
        popular_articles_like_count = popular_articles_div.find("span", class_=re.compile("^Like_counter_")).text
        print(str(index+1) + ":" + popular_articles_title)
        print("likes : " + popular_articles_like_count)
        print("")


if __name__ == '__main__':
    main()
