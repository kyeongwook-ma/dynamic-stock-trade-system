from task import *
from datamodel import *

class MainController(object):

    def __init__(self):
        super(MainController, self).__init__()
      

    def get_stock_value(self):
        for stock in stock_list:
            t = Task(parsing_stocks , stock)
            TaskController().enqueue_task(t)
        StockDataModel().add_data(self.task_ctlr.deque_task(), True)
        StockDataModel().print_all_model()

m = MainController()
m.get_stock_value()
