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
    
    print("Process Data...")
    df = TransToAdjOHLCbyAdjC(GetStockPriceVolumeData("DIS", gv.StockDataPoolPath, "2000-1-3", "2018-6-01", True))
    
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
    ChangeN.rename('Change'+str(change_rate)+'%', inplace=True)

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
    
    print('DataSize: {0}'.format(len(ChangeN)))
    
    print("Process Data finished.")
    
    OutputData = pandas.concat([ df, ChangeN], axis=1)
    OutputData.to_csv("C:\\zmcx16\\PredTrendA_data.csv", sep=',');
    
    vParam = {ValidationType.BlockCount: 3}
    RunValidation(df, ChangeN, ValidationType.ForwardingBlocks, vParam)

def PredTrendB(param):
    
    neighbor_size = 5
    pred_days = 5
    validateDataSize = 3
    
    print("Process Data...")
    df = TransToAdjOHLCbyAdjC(GetStockPriceVolumeData("DIS", gv.StockDataPoolPath, "2000-1-3", "2018-6-01", True))
    
    df = AddNeighborFeatures(df, neighbor_size, DropNan = False)
    
    df = AddChangeIndictor(df, strClose, DropNan = False)
    df = AddChangeIndictor(df, strVolume, DropNan = False)
    df = AddDiffIndictor(df, strClose, DropNan = False)
    df = AddDiffIndictor(df, strVolume, DropNan = False)
    df = AddLogReturnIndictor(df, strClose, DropNan = False)
    
    df = AddRollingMinMaxIndictor(df, strLow, window=5, Min0_Max1=0, DropNan = False)
    df = AddRollingMinMaxIndictor(df, strHigh, window=5, Min0_Max1=1, DropNan = False)
             
    df = AddSMAIndictor(df, window=5, DropNan = False)
    df = AddEMAIndictor(df, window=5, DropNan = False)
    df = AddMSTDIndictor(df, window=5, DropNan = False)
    df = AddMVARIndictor(df, window=5, DropNan = False)
    df = AddRSIIndictor(df, window=14, DropNan = False)
    
    df = AddBollingerBandsIndictor(df, window=5, DropNan = False)
    df = AddKDJIndictor(df, window=5, DropNan = False)
    
    
    df = df.dropna()
    
    #print(df)
    
    RollingVal = pandas.Series.rolling(df[strClose], window = pred_days, center = False).mean()

    UpOrDown = pandas.Series(numpy.zeros(shape=(df[strClose].count()),dtype=int), index=df.index)
    UpOrDown.rename(strUpOrDown, inplace=True)

    tmp_index = 0
    for i,v in UpOrDown.items():
        pred_index = tmp_index+pred_days
        if pred_index < UpOrDown.count():   
            if RollingVal.iloc[pred_index] < df[strClose][i]:
                UpOrDown[i] = -1
            else:
                UpOrDown[i] = 1
                
        else:
            UpOrDown[i] = UpOrDown.iloc[tmp_index-1]
        
        tmp_index+=1
        
    print(df)     
    print(UpOrDown)
    
    print('DataSize: {0}'.format(len(UpOrDown)))
    
    print("Process Data finished.")
        
    print("split Tr, Ts Data...")
    ValidateDataList = []
    
    TempData = df.copy()
    TempTarget = UpOrDown.copy();
    SplitSize = int(len(df.index) / validateDataSize)
    print('SplitSize: {0}, Total Size: {1}'.format(SplitSize, len(df.index)))
    for i in range(validateDataSize-1):
        data_t = TempData[:SplitSize]
        target_t = TempTarget[:SplitSize]
        ValidateDataList.append({strData: data_t, strTarget: target_t})
        TempData = TempData[SplitSize:]
        TempTarget = TempTarget[SplitSize:]
    
    
    ValidateDataList.append({strData: TempData, strTarget: TempTarget})    
    
    """
    x_train, x_test, y_train, y_test = train_test_split(df, IsChangeN, test_size=0.5)
    ValidateDataList.append({strData: x_train, strTarget: y_train}) 
    ValidateDataList.append({strData: x_test, strTarget: y_test}) 
    """
    
    #print(ValidateDataList)
    
    print("split Tr, Ts over.")
    
    print("Training & Testing Model...")
    
    ValidateResult = []
    for index in range(len(ValidateDataList)-1):
        print("Training & Testing Model{0}...".format(index))
        
        x_train = ValidateDataList[index][strData]
        y_train = ValidateDataList[index][strTarget]       
        x_test = ValidateDataList[index+1][strData]
        y_test = ValidateDataList[index+1][strTarget]

        #print(len(y_train))
        #print(sum(y_train))
        
        scaler = preprocessing.StandardScaler().fit(x_train)               
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)    
     
        #clf= KNeighborsClassifier(n_neighbors=3)
        #clf = LinearSVC(random_state=0) 
        #clf = GaussianNB() 
        #clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        #clf = DecisionTreeClassifier(random_state=0)
        clf = GaussianProcessClassifier(kernel=1.0 * kernels.RBF(length_scale=1.0))
        clf.fit(x_train, y_train) 
        predict_result = clf.predict(x_test).tolist()       

        
        ValidateResult.append({strPredictVal: predict_result, strAnsVal: y_test.tolist()})        
        
        print("Training & Testing Model{0} finished".format(index))
    
    print("Training & Testing finished.")
    
    #print(ValidateResult)
    
    total_result = {strPredictVal:[], strAnsVal:[]}
    for index in range(len(ValidateResult)):
        total_result[strPredictVal] = total_result[strPredictVal] + ValidateResult[index][strPredictVal]
        total_result[strAnsVal] = total_result[strAnsVal] + ValidateResult[index][strAnsVal]
    
    #print(total_result)
    
    ShowSensitivitySpecificity(total_result[strAnsVal], total_result[strPredictVal])
        
 
PredTrendFuncDict = {
  strPredTrendA:   {strFuncName: PredTrendA, strParam:{}},
  strPredTrendB:   {strFuncName: PredTrendB, strParam:{}}  
}
