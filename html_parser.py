import urllib

from bs4 import BeautifulSoup


def parsing_stocks(item):
    url = "http://stock.daum.net/item/main.daum?code=" + item
    soup = BeautifulSoup(urllib.urlopen(url).read())
    return soup.find("ul", "list_stockrate").contents[1].contents[0].encode_contents()

