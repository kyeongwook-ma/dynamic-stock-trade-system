import os
import math
from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from stock_list import *

os.chdir('./anni')
l = locals()

combined_list = list(map(lambda x : x + '.csv', stock_list))

for i in range(0,len(combined_list)):
        l['s_%d' % i] = pd.read_csv(combined_list[i])
        l['Close_s_%d' %i] = l['s_%d' % i].Close
        l['log_s_%d' %i] = np.log(l['Close_s_%d' % i])


def y_cointegration(asset1, asset2):
    return np.cov(asset2, asset1)[0][1] / np.var(asset2)

def spread(asset1, asset2):
    return asset1 - coint * asset2

def adfTest(spread):
    return ts.adfuller(spread, 1)[1]

for i in range(1,len(combined_list)-1):
    for j in range(i+1,len(combined_list)):        
        coint = y_cointegration('log_s_%d' %i, 'log_s_%d' %j)
        l['coint_%d' %i] = coint
        spread = spread('log_s_%d' %i, 'log_s_%d' %j)
        ADF_p_value = adfTest(spread)

        if ADF_p_value <= 0.05:
            print    "The spread is likely mean-reverting."
        else:
            print    "The spread is not mean-reverting."

        spread = Series(spread)
        signalMean = spread.mean()
        signalDev = spread.std()

        openMult = 1.0
        closeMult = 0.5
        stopLossMult = 4.0

        openSignal = signalDev * openMult;
        closeSignal = signalDev * closeMult;
        stopLossSignal = signalDev * stopLossMult;

        residSpread = spread - signalMean
        residSpread.plot()

        def plotSig(up,down,sig):
            up = sig * (residSpread * 0 + 1) 
            down = -sig * (residSpread * 0 + 1)
            up.plot()
            down.plot() 
        
        plotSig(openSignalUp, openSignalDown,openSignal)
        plotSig(closeSignalUp, closeSignalDown, closeSignal)
        plotSig(stopLossSignalup, stopLossSignalDown, stopLossSignal)


# this code will be updated.


#def permutations(items, n):
#    if n==0: yield []
#    else:
#        for i in xrange(len(items)):
#            for cc in permutations(items[:i]+items[i+1:],n-1):
#                yield [items[i]]+cc
#
#b = list(permutations(range(48), 2))



