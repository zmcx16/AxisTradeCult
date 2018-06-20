from builtins import int
from enum import Enum
from numpy import NaN
import random

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
from sklearn.calibration import CalibratedClassifierCV
from imblearn.over_sampling import RandomOverSampler
from attr._make import validate

import Program.GlobalVar as gv
from CommonDef.DefStr import *
from Program.Common import *
from Program.ProcessData import *
from Statistics_TechIndicators.CalcStatistics import *
from AxisPrediction.Backtest import *

def ForwardingBlocksValidation(Data, Target, BlockCount):
    
    OriginalCash = 50000
    perShareSize = 100
    backtestParam = {BacktestParam.strStrategyParams: 
                     {BacktestParam.strBuyStrategy: BacktestParam.BuyFixed
                      , BacktestParam.strSellStrategy: BacktestParam.SellAll
                      , BacktestParam.perShareSize: perShareSize}}
    backtest = Backtest(OriginalCash, False, backtestParam)
     
    print("split Tr, Ts Data...")
    ValidateDataList = []
    
    TempData = Data.copy()
    TempTarget = Target.copy();
    SplitSize = int(len(Data.index) / BlockCount)
    print('SplitSize: {0}, Total Size: {1}'.format(SplitSize, len(Data.index)))
    for i in range(BlockCount-1):
        data_t = TempData[:SplitSize]
        target_t = TempTarget[:SplitSize]
        ValidateDataList.append({strData: data_t, strTarget: target_t})
        TempData = TempData[SplitSize:]
        TempTarget = TempTarget[SplitSize:]
    
    
    ValidateDataList.append({strData: TempData, strTarget: TempTarget})    
    
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
                
        scaler = preprocessing.StandardScaler().fit(x_train)               
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)    
        
        # Binarize the output
        y_train = label_binarize(y_train, classes=[-1, 0, 1])
        y_test = label_binarize(y_test, classes=[-1, 0, 1])
        
        #clf= OneVsRestClassifier(KNeighborsClassifier(n_neighbors=5))
        #clf = OneVsRestClassifier(LinearSVC(random_state=0))
        #clf = OneVsRestClassifier(GaussianNB())
        #clf = OneVsRestClassifier(MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1))
        clf = OneVsRestClassifier(DecisionTreeClassifier(random_state=0))
        #clf = OneVsRestClassifier(GaussianProcessClassifier(kernel=1.0 * kernels.RBF(length_scale=1.0)))
        clf.fit(x_train, y_train)
        
        try:
            predict_prob = clf.predict_proba(x_test)
        except Exception as exc:
            print('Generated an exception: %s' % exc)
            predict_prob = clf.decision_function(x_test)
        
        #for index in range(len(predict_prob)):    
        #    print(predict_prob[index])
        
        # OvR clf.predict may produce [0 0 0] when prob equal: [0.4 0.4 0.2], we calculate by predict_proba
        class_labels = [-1, 0, 1]
        max_prob_index_list = predict_prob.argmax(axis=1)
        temp = []
        for i in range(len(max_prob_index_list)):
            temp.append(class_labels[max_prob_index_list[i]])
        predict_result = label_binarize(temp, class_labels)
        
        #print("predict_result:")
        for i in range(len(predict_result)):
            date = ValidateDataList[index+1][strData].iloc[i].name
            close = ValidateDataList[index+1][strData].iloc[i][strClose]
            high = ValidateDataList[index+1][strData].iloc[i][strHigh]
            low = ValidateDataList[index+1][strData].iloc[i][strLow]
            params = {strDate: date, strClose: close, strHigh: high, strLow: low}
            #print("{0}: {1}".format(date, predict_result[i]))
                        
            if predict_result[i][0] == 1:
                backtest.RunStrategy(BacktestParam.BuySignal, BacktestParam.EasyStrategy, params)
            elif predict_result[i][2] == 1:     
                backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params)
           
        backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params)    
        print("----------------")
        
        ValidateResult.append({strPredictVal: predict_result, strAnsVal: y_test, strPredictProbVal: predict_prob})        
        
        print("Training & Testing Model{0} finished".format(index))
    
    print("Training & Testing finished.")
    
    FinalCash = backtest.Cash
    Profit = FinalCash - OriginalCash
    print("Profit: {0}".format(Profit)) 
    print("ROI: {:.2%}".format(Profit/OriginalCash))     
    #print(ValidateResult)
    
    total_result = {strPredictVal:ValidateResult[0][strPredictVal], strPredictProbVal:ValidateResult[0][strPredictProbVal], strAnsVal:ValidateResult[0][strAnsVal]}
    for index in range(1, len(ValidateResult)):
        total_result[strPredictVal] = numpy.concatenate((total_result[strPredictVal], ValidateResult[index][strPredictVal]), axis=0)
        total_result[strPredictProbVal] = numpy.concatenate((total_result[strPredictProbVal], ValidateResult[index][strPredictProbVal]), axis=0)
        total_result[strAnsVal] = numpy.concatenate((total_result[strAnsVal], ValidateResult[index][strAnsVal]), axis=0)
    
    #print(total_result)
    
    ShowSensitivitySpecificityForMultiLabels(total_result[strAnsVal], total_result[strPredictVal], total_result[strPredictProbVal], [1, 0, -1])
    

def RunValidation(Data, Target, type, param):
    
    if ValidationType.ForwardingBlocks == type:
        ForwardingBlocksValidation(Data, Target, param[ValidationType.BlockCount])
    


class ValidationType(Enum):
    ForwardingBlocks = 1
    ForwardingLeaveOneOut = 2
    BlockCount = 'BlockCount'

    