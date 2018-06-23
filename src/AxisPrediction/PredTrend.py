import Program.GlobalVar as gv
from CommonDef.DefStr import *
from Program.Common import *
from Program.ProcessData import *
from AxisPrediction.Validation import *
from builtins import int
from numpy import NaN
from Statistics_TechIndicators.CalcStatistics import *

from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import *
from sklearn.svm import *
from sklearn.naive_bayes import *
from sklearn.neural_network import *
from sklearn.tree import *
from sklearn.gaussian_process import *
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from imblearn.over_sampling import RandomOverSampler
from attr._make import validate

def PredTrendA(param):
    
    neighbor_size = 10
    pred_days = 5
    change_rate = 5
    
    ClassLabel = 'Change'+str(change_rate)+'%'
    
    print("Process Data...")
    df = TransToAdjOHLCbyAdjC(GetStockPriceVolumeData("DIS", gv.StockDataPoolPath, "2000-1-1", "2018-6-01", True))
    
    df = AddNeighborFeatures(df, neighbor_size, DropNan = False)
      
    df = AddChangeIndictor(df, strClose, DropNan = False)
    df = AddChangeIndictor(df, strVolume, DropNan = False)
    df = AddDiffIndictor(df, strClose, DropNan = False)
    df = AddDiffIndictor(df, strVolume, DropNan = False)
    df = AddLogReturnIndictor(df, strClose, DropNan = False)
    
    df = AddRollingMinMaxIndictor(df, strLow, window=20, Min0_Max1=0, DropNan = False)
    df = AddRollingMinMaxIndictor(df, strHigh, window=20, Min0_Max1=1, DropNan = False)
    
    df = AddSMAIndictor(df, window=20, DropNan = False)
    df = AddEMAIndictor(df, window=20, DropNan = False)
    df = AddSMMAIndictor(df, window=20, DropNan = False)
    df = AddDMAIndictor(df, 10, 50, DropNan = False)
    df = AddMSTDIndictor(df, window=12, DropNan = False)
    df = AddMVARIndictor(df, window=20, DropNan = False)   
    df = AddRSIIndictor(df, window=14, DropNan = False)
    df = AddMACDIndictor(df, fast_period=12, slow_period=26, signal_period=9, DropNan = False)
    df = AddWRIndictor(df, window=14, DropNan = False)
    df = AddCCIIndictor(df, window=20, DropNan = False)
    df = AddATRIndictor(df, window=20, DropNan = False)
    df = AddDMIIndictor(df, window=14, DropNan = False)
    df = AddTEMAIndictor(df, window=9, DropNan = False)
    df = AddVRIndictor(df, window=26, DropNan = False)
    
    df = AddBollingerBandsIndictor(df, window=20, DropNan = False)
    df = AddKDJIndictor(df, window=20, DropNan = True)  
    
    df = df.dropna()
    
    #print(df)
    
    RollingVal = pandas.Series.rolling(df[strClose], window = pred_days, center = False).mean()

    ChangeN = pandas.Series(numpy.zeros(shape=(df[strClose].count()),dtype=int), index=df.index)
    ChangeN.rename(ClassLabel, inplace=True)

    tmp_index = 0
    for i,v in ChangeN.items():
        pred_index = tmp_index+pred_days
        if pred_index < ChangeN.count():   
            change = (RollingVal.iloc[pred_index] - df[strClose][i]) / df[strClose][i] *100
            if change < -1*change_rate:
                ChangeN[i] = -1
            elif change > change_rate:
                ChangeN[i] = 1
            else:
                ChangeN[i] = 0
                
        else:
            ChangeN[i] = ChangeN.iloc[tmp_index-1]
        
        tmp_index+=1
        
    print(df)     
    print(ChangeN)
    
    print(ChangeN.value_counts())
    print('DataSize: {0}'.format(len(ChangeN)))
    
    print("Process Data finished.")
    
    OutputData = pandas.concat([ df, ChangeN], axis=1)
    OutputData.to_csv("C:\\zmcx16\\PredTrendA_data.csv", sep=',');
    
    vParam = {ValidationType.TrDataSize: 250}
    RunValidation(df, ChangeN, ValidationType.ForwardingLeaveOneOut, vParam)

 
PredTrendFuncDict = {
  strPredTrendA:   {strFuncName: PredTrendA, strParam:{}},
}
