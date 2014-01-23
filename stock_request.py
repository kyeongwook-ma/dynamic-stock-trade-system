import urllib2
import os

from task import Task, TaskController
from stock_list import stock_list


def get_anni_csv():
    file_list = list()
    csv_folder = './anni/'

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    def csv_download(code):
        url = 'http://www.google.com/finance/historical?q=KRX%3A' + code + '&output=csv'

        csv_name = csv_folder + stock + '.csv'

        file_list.append(csv_name)

        csv_file = urllib2.urlopen(url)
        output = open(csv_name, 'wb')
        output.write(csv_file.read())
        output.close()

    for stock in stock_list:
        TaskController().enqueue_task(Task(csv_download, stock))

    if TaskController().is_task_done():
        return file_list


get_anni_csv()