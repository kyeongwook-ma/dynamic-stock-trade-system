import urllib
import urllib2

from bs4 import BeautifulSoup
from stock_list import *
from task import TaskController

def parsing_stocks(item):
    url = 'http://stock.daum.net/item/main.daum?code=' + item
    soup = BeautifulSoup( urllib.urlopen( url ).read() )
    return soup.find("ul", "list_stockrate").contents[1].contents[0].encode_contents()

def get_anni_stockCSV(code):
     
    def csv_download(file_name) :
        url = 'http://www.google.com/finance/historical?q=KRX%3A' + code + '&output=csv'
        csv_file = urllib2.urlopen(url)

        output = open(file_name, 'wb')
        output.write(csv_file.read())
        output.close()

    file_name = './anni' + code + '.csv'
    file_list = []
    file_list.append(file_name)

    TaskController.enqueue_task(Task(csv_download, file_name))
    
    return file_list