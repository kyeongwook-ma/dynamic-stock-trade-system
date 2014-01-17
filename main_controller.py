from task import *
from datamodel import *

class MainController(object):

    def __init__(self):
        super(MainController, self).__init__()
        self.task_ctlr = TaskController()
        self.data_model = StockDataModel()

    def get_stock_value(self):
        for stock in stock_list:
            t = Task(stock, parsing_stocks)
            self.task_ctlr.enqueue_task(t)
        self.data_model.add_data(self.task_ctlr.deque_task(), True)
        self.data_model.print_all_model()

m = MainController()
m.get_stock_value()
