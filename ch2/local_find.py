import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get("http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html")
    soup = BeautifulSoup(resp.text, "html.parser")

    # h4List = soup.find_all("h4")
    # for h4 in h4List:
    #     print(h4.a.text)

    # h4CardTitles = soup.find_all('h4', class_='card-title')
    # for h4CardTitle in h4CardTitles:
    #     print(h4CardTitle.a.text)
    #
    # idMacP = soup.find(id='mac-p').text.strip()
    # print(idMacP)

    # how to get data attribute
    # dataFoo = soup.find('' , {'data-foo':'mac-foo'})
    # print(dataFoo['href'])

    divs = soup.findAll('div', 'content')
    for div in divs:
        divTexth6 = div.h6.text.strip()
        divTexth4 = div.h4.a.text.strip()
        divTextp = div.p.text.strip()
        divStrippedString = div.stripped_strings
        print([s for s in divStrippedString])
        print(divTexth6, divTexth4, divTextp)


if __name__ == '__main__':
    main()
