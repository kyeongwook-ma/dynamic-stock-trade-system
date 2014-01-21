import os
import math
from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from stock_list import *
import sys


os.chdir('../anni')
l = locals()
count = 0
dissatisfired_adf_test = arange(10)
combined_list = list(map(lambda x : x + '.csv', filter(lambda x: x != '035420', stock_list)))


# a simple class with a write method

def adf_test(asset):
    return ts.adfuller(asset, 1)[1] 

satisfied_list = list()

# 우리가 쓰는게 공적분 방법인데 공적분을 쓰려면 시계열이 미리 안정적이면 안됨. 불안정한 것을 공적분해서 안정화 시키는 것이 목적이기 때문.
# 따라서 미리 안정한(stationary) 주가 목록을 제외하고 우리가 쓸수 있는 주가 목록을 추출하고자 함. 
for i in range(0,len(combined_list)):
    l['a_%d' % i] = pd.read_csv(combined_list[i])
    l['Close_a_%d' %i] = l['a_%d' % i].Close
    if adfTest(l['Close_a_%d' % i]) >= 0.05:
        print >> satisfied_list, combined_list[i]

for i in range(0,len(satisfied_list)):
    l['s_%d' % i] = pd.read_csv(satisfied_list[i])
    l['Close_s_%d' %i] = l['s_%d' % i].Close
    l['log_s_%d' %i] = np.log(l['Close_s_%d' % i])

# 아래 공적분 구하는 공식은 약식임. 재대로 구하려면 복잡함에따라 머신러닝이나 시뮬레이션 기법을 활용해야함. 
def y_cointegration(asset1, asset2):
    return np.cov(asset2, asset1)[0][1] / np.var(asset2)


for i in range(0,len(satisfied_list)-1):
    for j in range(i+1,len(satisfied_list)):        
        l['coint_%d' %i] = y_cointegration(l['log_s_%d' %i], l['log_s_%d' %j])
        spread = l['log_s_%d' %i] - l['coint_%d' %i] * l['log_s_%d' %j]
        ADF_p_value = adfTest(spread)
        if ADF_p_value <= 0.05:
            print    "The spread is likely mean-reverting , p-value of ADF Test is ", ADF_p_value
        else:
            print    "The spread is not mean-reverting , p-value of ADF Test is ", ADF_p_value 
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

        def plotSig(signal):
            up = signal * (residSpread * 0 + 1) 
            down = -signal * (residSpread * 0 + 1)
            up.plot()
            down.plot() 
            residSpread.plot()
            
        plotSig(openSignal)
        plotSig(closeSignal)
        plotSig(stopLossSignal)


