import pandas
import numpy
from itertools import islice
from CommonDef.DefStr import *
from Statistics_TechIndicators.CalcTechIndictors import *

def AddAdjOHLbyAdjC(srcData):
    dstData = srcData.copy()
    adjClose_offset = srcData[strAdjClose] - srcData[strClose]
    
    dstData[strAdjOpen] = pandas.Series(srcData[strOpen]+adjClose_offset, index=srcData.index)
    dstData[strAdjHigh] = pandas.Series(srcData[strHigh]+adjClose_offset, index=srcData.index)
    dstData[strAdjLow] = pandas.Series(srcData[strLow]+adjClose_offset, index=srcData.index)
    
    return dstData

def TransToAdjOHLCbyAdjC(srcData):
    dstData = srcData.copy()
    adjClose_scale = srcData[strAdjClose] / srcData[strClose]
    
    dstData[strOpen] *= adjClose_scale
    dstData[strHigh] *= adjClose_scale
    dstData[strLow] *= adjClose_scale
    dstData[strClose] = srcData[strAdjClose]
    dstData = dstData.drop(columns=[strAdjClose])
    
    return dstData

def AddNeighborFeatures(srcData, neighbor_size, DropNan = True):
    dstData = srcData.copy()    
    neighborsData = {}
    
    start_index = neighbor_size
    for index, row in islice(dstData.iterrows(), start_index, None):
        for i in range(neighbor_size):
            neighborsData[strNeighbor+str(i)] = dstData.shift(i+1)
    
    for i in range(neighbor_size):
        for col_name in list(dstData):
            neighborsData[strNeighbor+str(i)].rename(columns={col_name: col_name+'_N'+str(i)}, inplace=True)
            
    for neighbor_key in neighborsData:
        dstData = dstData.join(neighborsData[neighbor_key])

    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

# SMA: simple moving average
def AddSMAIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    SMA = GetRollingMean(srcData[strClose], window).to_frame()
    SMA.rename(columns= {strClose: strSMA+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(SMA)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

# EMA: exponential moving average
def AddEMAIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    EMA = GetEWM_Mean(srcData[strClose], window).to_frame()
    EMA.rename(columns= {strClose: strEMA+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(EMA)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData     

# MSTD: moving standard deviation
def AddMSTDIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    MSTD = GetRollingStd(srcData[strClose], window).to_frame()
    MSTD.rename(columns= {strClose: strMSTD+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(MSTD)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData   

# MVAR: moving variance
def AddMVARIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    MVAR = GetRollingVar(srcData[strClose], window).to_frame()
    MVAR.rename(columns= {strClose: strMVAR+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(MVAR)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

# RSV: raw stochastic value
def AddRSVIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    RSV = GetRSV(srcData[strClose], srcData[strHigh], srcData[strLow], window).to_frame()
    RSV.rename(columns= {strClose: strRSV+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(RSV)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

# RSI: relative strength index
def AddRSIIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    RSI = GetRSI(srcData[strClose], window).to_frame()
    RSI.rename(columns= {strClose: strRSI+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(RSI)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

def AddBollingerBandsIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    MA_mean = GetRollingMean(srcData[strClose], window)
    MA_std = GetRollingStd(srcData[strClose], window)
    upper_band, lower_band = GetBollingerBands(MA_mean, MA_std)
    upper_band.rename(strBollingerBand_upper+'_W'+str(window), inplace=True)
    lower_band.rename(strBollingerBand_lower+'_W'+str(window), inplace=True)
    BollingerBands = pandas.concat([upper_band,lower_band], axis=1)

    dstData = dstData.join(BollingerBands)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

def AddKDJIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    k, d, j = GetKDJ(srcData[strClose], srcData[strHigh], srcData[strLow], window)

    k.rename(strKDJ_K+'_W'+str(window), inplace=True)
    d.rename(strKDJ_D+'_W'+str(window), inplace=True)
    j.rename(strKDJ_J+'_W'+str(window), inplace=True)

    KDJ = pandas.concat([k,d,j], axis=1)
    KDJ.set_index(srcData.index.values, inplace = True)
    
    dstData = dstData.join(KDJ)
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
    
    return dstData

def AddChangeIndictor(srcData, srcName, DropNan = True):
    #gross return
    dstData = srcData.copy()
    
    dstData["{0}_{1}".format(srcName,strChangeRate)] = GetChange(srcData[srcName])
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
        
    return dstData

def AddDiffIndictor(srcData, srcName, DropNan = True):
    dstData = srcData.copy()
    
    dstData["{0}_{1}".format(srcName,strChangeRate)] = GetDiff(srcData[srcName])
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
        
    return dstData

def AddLogReturnIndictor(srcData, srcName, DropNan = True):
    dstData = srcData.copy()
    dstData["{0}_{1}".format(srcName,strLogReturn)] = GetLogReturn(srcData[srcName])
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
        
    return dstData

def AddRollingMinMaxIndictor(srcData, srcName, window, Min0_Max1, DropNan = True):
    dstData = srcData.copy()
    if Min0_Max1 == 0:
        dstData["{0}_{1}_W{2}".format(srcName, strRollingMin, window)] = GetRollingMin(srcData[srcName], window)
    else:
        dstData["{0}_{1}_W{2}".format(srcName, strRollingMax, window)] = GetRollingMax(srcData[srcName], window)
    
    if DropNan:
        dstData = dstData.dropna(axis=0, how='any')
        
    return dstData
