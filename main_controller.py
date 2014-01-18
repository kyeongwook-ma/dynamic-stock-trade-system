from datamodel import StockDataModel
from stock_request import *


class MainController(object):
    def __init__(self):
        super(MainController, self).__init__()

    @staticmethod
    def get_stock_value():
        get_rt_stocks()
        StockDataModel().add_data(TaskController().deque_task(), True)

