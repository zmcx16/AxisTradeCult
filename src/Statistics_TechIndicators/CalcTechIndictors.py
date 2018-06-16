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

def GetSMMA(values, window):
    return values.ewm(ignore_na=False, alpha=1.0 / window, min_periods=0, adjust=True).mean()

def GetDMA(values, short_window=10, long_window=50):
    return GetRollingMean(values, short_window)-GetRollingMean(values, long_window)

def GetRSV(close_values, high_values, low_values, period):
    hight_max = pandas.Series.rolling(high_values, window = period, center = False).max()
    low_min = pandas.Series.rolling(low_values, window = period, center = False).min()
    return (close_values - low_min) / (hight_max - low_min) * 100

def GetRSI(values, window):
    values_shift_1 = values.shift(1)
    d = values - values_shift_1
    p = (d + d.abs()) / 2
    n = (-d + d.abs()) / 2
    
    RS = GetEMA(p, window = window) / GetEMA(n, window = window)
    
    return 100 - 100 / (1.0 + RS)

def GetMACD(values, fast_period, slow_period, signal_period):
    DIF = GetEMA(values, fast_period) - GetEMA(values, slow_period)
    DEM = GetEMA(DIF, signal_period)
    OSC = DIF - DEM
    return DIF, DEM, OSC

def GetWR(values, window):
    hn = pandas.Series.rolling(values, window = window, center = False).max()
    ln = pandas.Series.rolling(values, window = window, center = False).min()     
    return (values-hn)/(hn-ln)*100

def GetCCI(close_values, high_values, low_values, window): 
    TP = (high_values+low_values+close_values)/3
    SMA = pandas.Series.rolling(TP, window = window, center = False).mean()
    MD = TP.rolling(window=window, center=False).apply(lambda x: numpy.fabs(x - x.mean()).mean(), raw=True)
    return  (TP - SMA) / (.015 * MD)

def GetTR(close_values, high_values, low_values): 
    prev_close = close_values.shift(1)
    prev_close.fillna(value=0, inplace=True)
    c1 = high_values - low_values
    c2 = numpy.abs(high_values - prev_close)
    c3 = numpy.abs(low_values - prev_close)
    return numpy.max((c1, c2, c3), axis=0)

def GetATR(close_values, high_values, low_values, window): 
    TR = GetTR(close_values, high_values, low_values)
    TR_series = pandas.Series(TR, index = close_values.index)
    return GetSMMA(TR_series, window)

def GetDMI(close_values, high_values, low_values, window=14):
    UpMove = high_values - high_values.shift(1)
    DownMove = low_values.shift(1) - low_values
        
    pDM = pandas.Series(numpy.zeros(shape=(close_values.count()),dtype=float), index=close_values.index)
    nDM = pandas.Series(numpy.zeros(shape=(close_values.count()),dtype=float), index=close_values.index)
    for i,v in close_values.items():
        if UpMove[i] > DownMove[i] and UpMove[i] > 0:
            pDM[i] = UpMove[i]
        else:
            pDM[i] = 0
            
        if DownMove[i] > UpMove[i] and DownMove[i] > 0:
            nDM[i] = DownMove[i]
        else:
            nDM[i] = 0
                   
    pDI = 100 * GetEMA(pDM, window) / GetATR(close_values, high_values, low_values, window)
    nDI = 100 * GetEMA(nDM, window) / GetATR(close_values, high_values, low_values, window)
    
    DX = 100 * numpy.fabs((pDI - nDI) / (pDI + nDI))
    ADX = GetEMA(DX, window)
    ADXR = GetEMA(ADX, window)
    
    return pDI, nDI, ADX, ADXR

def GetTRIX(values, window):
    triple = GetEMA(GetEMA(GetEMA(values, window), window), window)
    prev_triple = triple.shift(1)
    return (triple-prev_triple) * 100 / prev_triple

def GetVR(close_values, volume_values, window):
   
    prev_close = close_values.shift(1)
    
    av = pandas.Series(numpy.where(close_values-prev_close>0, volume_values, 0), index=close_values.index)
    avs = pandas.Series.rolling(av, window = window, center = False).sum()
    
    bv = pandas.Series(numpy.where(close_values-prev_close<0, volume_values, 0), index=close_values.index)
    bvs = pandas.Series.rolling(bv, window = window, center = False).sum()
    
    cv = pandas.Series(numpy.where(close_values-prev_close==0, volume_values, 0), index=close_values.index)
    cvs = pandas.Series.rolling(cv, window = window, center = False).sum()
    
    return  (avs + cvs / 2) / (bvs + cvs / 2) * 100
    
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

