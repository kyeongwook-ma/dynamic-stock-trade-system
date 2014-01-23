import os

from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from stock_list import *


os.chdir('../anni')


def adf_test(asset):
    return ts.adfuller(asset, 1)[1]


def y_cointegration(asset1, asset2):
    return np.cov(asset2, asset1)[0][1] / np.var(asset2)


def plot_sig(signal, spread):
    up = signal * (spread * 0 + 1)
    down = -signal * (spread * 0 + 1)
    up.plot()
    down.plot()
    spread.plot()


class Pair(object):
    """docstring for Pair"""

    def __init__(self):
        super(Pair, self).__init__()
        self._list = list(map(lambda x: x + '.csv', filter(lambda x: x != '035420', stock_list)))
        self.satisfied_list = list()
        self.spread = 0
        self.signal_mean = 0
        self.signal_dev = 0
        self.open_mult = 1.0
        self.close_mult = 0.5
        self.stoploss_mult = 4.0
        self.open_signal = 0
        self.close_signal = 0
        self.stoploss_signal = 0
        self.resid_spread = 0
        self.ADF_p_value = 0

    def check_adf(self):
        for i in range(0, len(self._list)):
            origin = pd.read_csv(self._list[i]).Close

            if adf_test(origin) >= 0.05:
                loged = np.log(origin)
                self.satisfied_list.append(loged)

    def create_pair(self):
        for i in range(0, len(self.satisfied_list) - 1):
            for j in range(i + 1, len(self.satisfied_list)):

            coint = y_cointegration(self.satisfied_list[i], self.satisfied_list[j])

            self.spread = self.satisfied_list[i] - coint * self.satisfied_list[j]
            ADF_p_value = adf_test(self.spread)

            if self.ADF_p_value <= 0.05:
                print    "The spread is likely mean-reverting , p-value of ADF Test is ", ADF_p_value
            else:
                print    "The spread is not mean-reverting , p-value of ADF Test is ", ADF_p_value

            self.spread = Series(self.spread)
            self.signal_mean = self.spread.mean()
            self.signal_dev = self.spread.std()
            self.open_mult = 1.0
            self.close_mult = 0.5
            self.stoploss_mult = 4.0
            self.open_signal = self.signalDev * self.openMult
            self.close_signal = self.signalDev * self.closeMult
            self.stoploss_signal = self.signalDev * self.stopLossMult
            self.resid_spread = self.spread - self.signalMean




