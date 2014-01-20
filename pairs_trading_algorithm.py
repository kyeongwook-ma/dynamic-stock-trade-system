import os
import math
from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts


class Mylist(list):
    def __mul__(self,other):
        return [[s,o] for s in self for o in other]


stock_list = Mylist(
    [
    '005930', '005380', '005490', '012330',
    '000660', '035420', '005935', '015760',
    '055550', '032830', '051910', '009540',
    '017670', '105560', '096770', '023530',
    '086790', '000810', '066570', '003550',
    '053000', '033780', '000830', '034220',
    '003600', '010140', '086280', '051900',
    '010950', '030200', '011170', '161390',
    '139480', '004020', '006400', '042660',
    '000720', '024110', '035250', '034730',
    '036460', '088350', '010130', '090430',
    '001800', '036570', '009150', '078930'
    ]
)

append_csv = Mylist(['.csv'])

combined_list = stock_list * append_csv

for i in range(len(combined_list)):
    combined_list[i] = ''.join(combined_list[i])

l = locals()
for i in range(0,len(combined_list)):
        l['s_%d' % i] = pd.read_csv(combined_list[i])
        l['Close_s_%d' %i] = l['s_%d' % i].Close
        l['log_s_%d' %i] = log(l['Close_s_%d' % i])


#현재 이중 for 문에서 애러가 나고 있음.
#아래 코드의 목적은 48개의 주가에 1128개의 조합이 있는데 이들을 매치시키고자 하는 작업임. 그러나 현재 애러 상태 . 
for i in range(1,len(combined_list)-1):
    for j in range(i+1,len(combined_list)):        

        def y_cointegration('log_s_%d' %i, 'log_s_%d' %j):
            coint_result = np.cov('log_s_%d' %j, 'log_s_%d' %i)[0][1] / np.var('log_s_%d' %j)
            return coint_result

        coint = y_cointegration('log_s_%d' %i, 'log_s_%d' %j)
        l['coint_%d' %i] = coint

        def spread('log_s_%d' %i, 'log_s_%d' %j):
            spread = 'log_s_%d' %i - coint * 'log_s_%d' %j
            return spread

        spread = spread('log_s_%d' %i, 'log_s_%d' %j)


        def adfTest(spread):
            ADF_p_value = ts.adfuller(spread, 1)[1]
            return ADF_p_value

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