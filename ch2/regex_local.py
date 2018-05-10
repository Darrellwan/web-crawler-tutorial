import requests
import re
from bs4 import BeautifulSoup


def main():
    resp = requests.get('http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html')
    soup = BeautifulSoup(resp.text, 'html.parser')

    # find all html tag start with h
    # titles = soup.find_all(['h1','h2','h3','h3','h5','h6'])
    # another way with regular expression
    # titles = soup.find_all(re.compile('h[1-6]'))
    # for title in titles:
    #     print(title.text.strip())

    # find all picture with png ending
    # imgs = soup.find_all('img')
    # for img in imgs:
    #     if 'src' in img.attrs:
    #         if img['src'].endswith('.png'):
    #             print(img['src'])
    # another way in regular expression
    # for img in soup.find_all('img', {'src': re.compile('\.png$')}):
    #     print(img['src'])

    # find picture with file name contain beginner and end with png
    # imgs = soup.find_all('img')
    # for img in imgs:
    #     if 'src' in img.attrs:
    #         if 'beginner' in img['src'] and img['src'].endswith('.png'):
    #             print(img['src'])

    # another way in reqular expression
    #for img in soup.find_all('img',{'src': re.compile('beginner.*\.png$')}):
    #    print(img['src'])





if __name__ == '__main__':
    main()
