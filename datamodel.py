from singleton import Singleton

class StockDataModel(object):

    __metaclass__ = Singleton

    def __init__(self):
        super(StockDataModel, self).__init__()
        self.data_list = []

    def add_data(self, stock, is_multiple = False, idx = 0 ):

        if is_multiple == True:
            self.data_list.extend(stock)
        else:
            self.data_list.append(stock)
        if idx != 0:
            self.data_list.index(stock, idx)

    def get_list_size(self):
        return len(self.data_list)

    def del_data(self, idx):
        self.data_list.pop(idx)

    def del_data(self, stock):
        self.data_list.remove(stock)

    def print_all_model(self):
        print self.data_list


