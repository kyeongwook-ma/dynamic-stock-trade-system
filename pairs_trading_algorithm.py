import os
import math

from pandas import Series
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts


os.chdir('C:\Users\Haneul\Desktop\Project\data')
os.getcwd()

df = pd.read_csv('RawData.csv')

samsungElec = df.SamsungElec
samsungLife = df.SamsungLife
kodex = df.Kodex
bond = df.Bond

length = len(df)

logSamsungElec = np.empty(length)
logSamsungLife = np.empty(length)
logKodex = np.empty(length)
logBond = np.empty(length)

for t in range(length):
    logSamsungElec[t] = math.log(samsungElec[t])
    logSamsungLife[t] = math.log(samsungLife[t])
    logKodex[t] = math.log(kodex[t])
    logBond[t] = math.log(bond[t])


def y_cointegration(logAsset1, logAsset2):
    coint_result = np.cov(logAsset2, logAsset1)[0][1] / np.var(logAsset2)
    return coint_result


coint = y_cointegration(logSamsungLife, logSamsungElec)


def spread(logAsset1, logAsset2):
    spread = logAsset1 - coint * logAsset2
    return spread


spread = spread(logSamsungElec, logSamsungLife)


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
