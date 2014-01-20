import os
import math
from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts


os.chdir('./anni')
l = locals()

stock_list = [
    '005930', '005380', '005490', '012330',
    '000660', '078930', '005935', '015760',
    '055550', '032830', '051910', '009540',
    '017670', '105560', '096770', '023530',
    '086790', '000810', '066570', '003550',
    '053000', '033780', '000830', '034220',
    '003600', '010140', '086280', '051900',
    '010950', '030200', '011170', '161390',
    '139480', '004020', '006400', '042660',
    '000720', '024110', '035250', '034730',
    '036460', '088350', '010130', '090430',
    '001800', '036570', '009150', 
    ]


combined_list = list(map(lambda x : x + '.csv', stock_list))


for i in range(0,len(combined_list)):
    l['s_%d' % i] = pd.read_csv(combined_list[i])
    l['Close_s_%d' %i] = l['s_%d' % i].Close
    l['log_s_%d' %i] = np.log(l['Close_s_%d' % i])




def y_cointegration(asset1, asset2):
    return np.cov(asset2, asset1)[0][1] / np.var(asset2)


def adfTest(spread):
    return ts.adfuller(spread, 1)[1] 


for i in range(0,len(combined_list)):
    for j in range(i+1,len(combined_list)+1):        
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
        def plotSig(signal,residSpread):
            up = signal * (residSpread * 0 + 1) 
            down = -signal * (residSpread * 0 + 1)
            up.plot()
            down.plot() 
            residSpread.plot()
        plotSig(openSignal, residSpread)
        plotSig(closeSignal, residSpread)
        plotSig(stopLossSignal, residSpread)


