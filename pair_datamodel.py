import os

from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from stock_list import *
from base_model import DataModel


os.chdir('../anni')


def adf_test(asset):
    return ts.adfuller(asset, 1)[1]


def get_cointegration(asset1, asset2):
    return np.cov(asset2, asset1)[0][1] / np.var(asset2)


def plot_sig(signal, spread):
    up = signal * (spread * 0 + 1)
    down = -signal * (spread * 0 + 1)
    up.plot()
    down.plot()
    spread.plot()


class Pair(object):
    """class for store some values"""

    def __init__(self, spread, sig_mean, sig_dev, open_mult, close_mult,
                 stoploss_mult, open_sig, close_sig, stoploss_sig,
                 resid_spread, p_value, coint):
        super(Pair, self).__init__()

        self.satisfied_list = list()
        self.spread = spread
        self.sig_mean = sig_mean
        self.sig_dev = sig_dev
        self.open_mult = open_mult
        self.close_mult = close_mult
        self.stoploss_mult = stoploss_mult
        self.open_sig = open_sig
        self.close_sig = close_sig
        self.stoploss_sig = stoploss_sig
        self.resid_spread = resid_spread
        self.p_value = p_value
        self.coint = coint


class PairDataModel(DataModel):
    """ inhert from datamodel for saving pair value """

    def __init__(self):
        super(PairDataModel, self).__init__()

    def create_pair(self):

        # examine adf_test and return logged values
        def check_adf():
            csv_list = list(map(lambda x: x + '.csv', filter(lambda x: x != '035420', stock_list)))
            satisfied_list = list()

            for i in range(0, len(csv_list)):
                # get data from csv file
                origin = pd.read_csv(csv_list[i]).Close

                # check condition and push into list
                if adf_test(origin) >= 0.05:
                    logged = np.log(origin)
                    satisfied_list.append(logged)
            return satisfied_list

            # get checked values
            pair_list = check_adf()

            # this loop looks like to be refactored
            for i in range(0, len(pair_list) - 1):
                for j in range(i + 1, len(pair_list)):

                    # get a coint value from two list contents
                    coint = get_cointegration(pair_list[i], pair_list[j])

                    ## do some math ...
                    spread = pair_list[i] - coint * pair_list[j]
                    p_value = adf_test(spread)

                    if p_value <= 0.05:
                        print "The spread is likely mean-reverting , p-value of ADF Test is ", p_value
                    else:
                        print "The spread is not mean-reverting , p-value of ADF Test is ", p_value

                    spread = Series(spread)
                    sig_mean = spread.mean()
                    sig_dev = spread.std()
                    open_mult = 1.0
                    close_mult = 0.5
                    stoploss_mult = 4.0
                    open_sig = sig_dev * open_mult
                    close_sig = sig_dev * close_mult
                    stoploss_sig = sig_dev * stoploss_mult
                    resid_spread = spread - sig_mean

                    # push into pair data model
                    self.add_data(Pair(spread=spread, sig_mean=sig_mean,
                                       sig_dev=sig_dev, open_mult=open_mult,
                                       close_mult=close_mult, stoploss_mult=stoploss_mult,
                                       open_sig=open_sig, close_sig=close_sig,
                                       stoploss_sig=stoploss_sig, resid_spread=resid_spread,
                                       p_value=p_value, coint=coint))


