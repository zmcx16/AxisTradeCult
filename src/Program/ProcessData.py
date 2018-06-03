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

def AddMAIndictor(srcData, window, DropNan = True):
    dstData = srcData.copy()
    MA = GetRollingMean(srcData[strClose], window).to_frame()
    MA.rename(columns= {strClose: strMA+'_W'+str(window)}, inplace=True)
    dstData = dstData.join(MA)
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
    