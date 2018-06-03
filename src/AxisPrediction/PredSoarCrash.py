import Program.GlobalVar as gv
from CommonDef.DefStr import *
from Program.Common import *
from Program.ProcessData import *
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
from imblearn.over_sampling import RandomOverSampler
from attr._make import validate

def PredSoarCrashA(param):
    # CrashA param
    neighbor_size = 5
    pred_days = 3
    change_rate = 5
    validateDataSize = 3
    
    IsSoar = False

    print("Process Data...")
    df = TransToAdjOHLCbyAdjC(GetStockPriceVolumeData("DIS", gv.StockDataPoolPath, "2000-1-3", "2018-6-01", True))
    
    df = AddMAIndictor(df, window=5, DropNan = False)
    df = AddBollingerBandsIndictor(df, window=5, DropNan = False)
    df = AddKDJIndictor(df, window=5, DropNan = False)
    #print(df)
    
    df = AddNeighborFeatures(df, neighbor_size, DropNan = True)
    #print(df)
    
    if IsSoar:
        SoarOrCrash = strIsSoar
        RollingVal = pandas.Series.rolling(df[strClose], window = pred_days, center = False).min()    
    else:
        SoarOrCrash = strIsCrash
        RollingVal = pandas.Series.rolling(df[strClose], window = pred_days, center = False).max()    
        
    IsChangeN = pandas.Series(numpy.zeros(shape=(df[strClose].count()),dtype=bool), index=df.index)
    IsChangeN.rename(SoarOrCrash+'_'+str(change_rate)+'%', inplace=True)

    tmp_index = 0
    for i,v in IsChangeN.items():
        pred_index = tmp_index+pred_days
        if pred_index < IsChangeN.count():   
            change = (RollingVal.iloc[pred_index] - df[strClose][i]) / df[strClose][i] *100
            if (change < -1*change_rate and not IsSoar) or (change > change_rate and IsSoar):
                IsChangeN[i] = True
        else:
            IsChangeN[i] = IsChangeN.iloc[tmp_index-1]
        
        tmp_index+=1
        
    #print(df)     
    #print(IsChangeN)
    
    print('DataSize: {0}, PostitiveSize: {1}'.format(len(IsChangeN), sum(IsChangeN)))
    
    print("Process Data finished.")
    
    OutputData = pandas.concat([ df, IsChangeN], axis=1)
    OutputData.to_csv("D:\\PredCrashA_data.csv", sep=',');
    
    print("split Tr, Ts Data...")
    ValidateDataList = []
    
    TempData = df.copy()
    TempTarget = IsChangeN.copy();
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
        
        # OverSamoling
        #ros = RandomOverSampler(random_state=0)
        #x_train, y_train = ros.fit_sample(x_train, y_train)
        
        #print(len(y_train))
        #print(sum(y_train))
        
        scaler = preprocessing.StandardScaler().fit(x_train)               
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)    

        
        #clf= KNeighborsClassifier(n_neighbors=3)
        #clf = LinearSVC(random_state=0) 
        #clf = GaussianNB() 
        #clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        clf = DecisionTreeClassifier(random_state=0)
        #clf = GaussianProcessClassifier(kernel=1.0 * kernels.RBF(length_scale=1.0))
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
    
 
PredCrashFuncDict = {
  strPredSoarCrashA:   {strFuncName: PredSoarCrashA, strParam:{}},
}
