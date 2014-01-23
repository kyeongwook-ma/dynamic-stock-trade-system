__author__ = 'zetyx'
from singleton import Singleton


class DataModel(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(DataModel, self).__init__()
        self.data_list = []

    def add_data(self, data, is_multiple=False, idx=0):

        if is_multiple is True:
            self.data_list.extend(data)
        else:
            self.data_list.append(data)
        if idx != 0:
            self.data_list.index(data, idx)

    def get_list_size(self):
        return len(self.data_list)

    def del_data(self, idx):
        self.data_list.pop(idx)

    def del_data(self, stock):
        self.data_list.remove(stock)

    def print_all_model(self):
        print self.data_list



