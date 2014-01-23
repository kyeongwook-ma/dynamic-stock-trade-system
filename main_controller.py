from rts_datamodel import RTSDataModel


class MainController(object):
    def __init__(self):
        super(MainController, self).__init__()

    @staticmethod
    def get_stock_value():
        RTSDataModel().get_rt_stocks()

