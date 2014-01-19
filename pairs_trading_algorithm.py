import os
import math
from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from stock_list import *

# 초기 설정
os.chdir('./anni')
l = locals()

combined_list = list(map(lambda x : x + '.csv', stock_list))

for i in range(len(combined_list)):
    combined_list[i] = ''.join(combined_list[i])

for i in range(0,len(combined_list)):
        l['s_%d' % i] = pd.read_csv(combined_list[i])
        l['Close_s_%d' %i] = l['s_%d' % i].Close
        l['log_s_%d' %i] = np.log(l['Close_s_%d' % i])


def y_cointegration(asset1, asset2):
    coint_result = np.cov(asset2, asset1)[0][1] / np.var(asset2)
    return coint_result

def spread(asset1, asset2):
    spread = asset1 - coint * asset2
    return spread

def adfTest(spread):
    ADF_p_value = ts.adfuller(spread, 1)[1]
    return ADF_p_value

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

        openSignalUp = openSignal * (residSpread * 0 + 1)
        openSignalDown = -openSignal * (residSpread * 0 + 1)
        openSignalUp.plot()
        openSignalDown.plot()

        closeSignalUp = closeSignal * (residSpread * 0 + 1)
        closeSignalDown = -closeSignal * (residSpread * 0 + 1)
        closeSignalUp.plot()
        closeSignalDown.plot()

        stopLossSignalup = stopLossSignal * (residSpread * 0 + 1)
        stopLossSignalDown = -stopLossSignal * (residSpread * 0 + 1)
        stopLossSignalup.plot()
        stopLossSignalDown.plot()


# this code will be updated.



## 안쓰는 자료 
# 원래 조합이 48C2 = 1128개여야 하는데 아래 알고리즘은 2256개로 불필요한 계산이 들어가 있음

#def permutations(items, n):
#    if n==0: yield []
#    else:
#        for i in xrange(len(items)):
#            for cc in permutations(items[:i]+items[i+1:],n-1):
#                yield [items[i]]+cc
#
#b = list(permutations(range(48), 2))



