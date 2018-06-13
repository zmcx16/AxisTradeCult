import pandas
import numpy


def GetRollingMean(values, window):
    return pandas.Series.rolling(values, window = window, center = False).mean()

def GetRollingStd(values, window):
    return pandas.Series.rolling(values, window = window, center = False).std()

def GetRollingMax(values, window):
    return pandas.Series.rolling(values, window = window, center = False).max()

def GetRollingMin(values, window):
    return pandas.Series.rolling(values, window = window, center = False).min()

def GetEMA(values, window):
    return values.ewm(span=window).mean()

def GetRSV(close_values, high_values, low_values, period):
    hight_max = pandas.Series.rolling(high_values, window = period, center = False).max()
    low_min = pandas.Series.rolling(low_values, window = period, center = False).min()
    return (close_values - low_min) / (hight_max - low_min) * 100

def GetRSI(values, window=14):
    values_shift_1 = values.shift(1)
    d = values - values_shift_1
    p = (d + d.abs()) / 2
    n = (-d + d.abs()) / 2
    
    RS = GetEMA(p, window = window) / GetEMA(n, window = window)
    
    return 100 - 100 / (1.0 + RS)

def GetMACD(values):
    DIF = GetEMA(values, 12) - GetEMA(values, 26)
    DEM = GetEMA(DIF, 9)
    OSC = DIF - DEM
    return DIF, DEM, OSC

def GetWR(values, window):
    hn = pandas.Series.rolling(values, window = window, center = False).max()
    ln = pandas.Series.rolling(values, window = window, center = False).min()
     
    return (values-hn)/(hn-ln)*100

def GetRollingVar(values, window):
    return values.rolling(window = window).var()

def GetLogReturn(values):
    return numpy.log(values) - numpy.log(values.shift(1))

def GetDiff(values):
    return values.diff()

def GetChange(values):
    return values.pct_change() * 100


def GetBollingerBands(rm, rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def GetKDJ(close_values, high_values, low_values, period):
    rsv = GetRSV(close_values, high_values, low_values, period)
    k = pandas.Series(_calc_kd(rsv))
    d = pandas.Series(_calc_kd(k))
    j = 3 * d - 2 * k

    return k, d, j


def _calc_kd(val, weight = 1 / 3.0):
    """
    k[0]=50
    for i in range(1,len(val)):     
        if pandas.isnull(val[i]):
            k[i] = 50
        else:
            k[i] = 2/3.0*k[i-1]+1/3.0*val[i]
    
    return k    
    """
    
    k = 50.0
    for i in weight * val:
        if pandas.isnull(i):
            yield k
        else:
            k = (1 - weight) * k + i
            yield k

