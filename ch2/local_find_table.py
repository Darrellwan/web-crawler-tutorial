import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get("http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html")
    soup = BeautifulSoup(resp.text, "html.parser")

    # prices = []
    # rows = soup.find('table', 'table').tbody.find_all('tr')
    # for row in rows :
    #     price = row.find_all('td')[2].text
    #     print(price)
    #     prices.append(int(price))

    #another way by sibling
    # prices = []
    # links = soup.findAll('a')
    # for link in links:
    #     price = link.parent.previous_sibling.text
    #     prices.append(int(price))
    # print(sum(prices)/len(prices))

    #get all page info
    # rows = soup.find('table' , 'table').tbody.find_all('tr')
    # for row in rows:
    #     # all_tds = row.find_all('td')
    #     all_tds = [td for td in row.children]
    #     if 'href' in all_tds[3].a.attrs:
    #         href = all_tds[3].a['href']
    #     else:
    #         href = None
    #     print(all_tds[0].text, all_tds[1].text, all_tds[2].text, href , all_tds[3].a.img['src'])

    # use stripped_strings
    rows = soup.find('table', 'table').tbody.find_all('tr')
    for row in rows:
        print([s for s in row.stripped_strings])



if __name__ == '__main__':
    main()
