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

def ForwardingLeaveOneOutValidation(Data, Target, TrDataSize):
    
    OriginalCash = 50000
    perShareSize = 100
    backtestParam = {BacktestParam.strStrategyParams: 
                     {BacktestParam.strBuyStrategy: BacktestParam.BuyFixed
                      , BacktestParam.strSellStrategy: BacktestParam.SellAll
                      , BacktestParam.perShareSize: perShareSize}}
    backtest = Backtest(OriginalCash, False, backtestParam)
     
    ValidateResult = []
    
    TsLength = len(Data.index) - TrDataSize
    print("TrData Size: {0}".format(TrDataSize))
    print("TsData Size: {0}".format(TsLength))   
    for i in range(TsLength):
        x_train = Data[i:TrDataSize+i]
        y_train = Target[i:TrDataSize+i]
        x_test = Data[TrDataSize+i:TrDataSize+i+1]
        y_test = Target[TrDataSize+i:TrDataSize+i+1]
                        
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
            #print('Generated an exception: %s' % exc)
            predict_prob = clf.decision_function(x_test)
        
        #for index in range(len(predict_prob)):    
        #    print(predict_prob[index])
        
        # OvR clf.predict may produce [0 0 0] when prob equal: [0.4 0.4 0.2], we calculate by predict_proba
        class_labels = [-1, 0, 1]
        max_prob_index_list = predict_prob.argmax(axis=1)
        temp = []
        for x in range(len(max_prob_index_list)):
            temp.append(class_labels[max_prob_index_list[x]])
        predict_result = label_binarize(temp, class_labels)
        
        date = Data.iloc[TrDataSize+i].name
        close = Data.iloc[TrDataSize+i][strClose]
        high = Data.iloc[TrDataSize+i][strHigh]
        low = Data.iloc[TrDataSize+i][strLow]
        params = {strDate: date, strClose: close, strHigh: high, strLow: low}

        if predict_result[0][0] == 1:
            backtest.RunStrategy(BacktestParam.BuySignal, BacktestParam.EasyStrategy, params)
        elif predict_result[0][2] == 1:   
            backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params)
               
        ValidateResult.append({strPredictVal: predict_result, strAnsVal: y_test, strPredictProbVal: predict_prob})        
        
        if i%100 == 0:
            print("Training & Testing Model{0} finished".format(i))
    
    print("Training & Testing finished.")
    
    backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params) 
    
    print("---Trade List----------------------")      
    backtest.PrintTradeList()
    print("-----------------------------------")     
    
    FinalCash = backtest.Cash
    Profit = FinalCash - OriginalCash
    print("Profit: {0}".format(Profit)) 
    print("ROI: {:.2%}".format(Profit/OriginalCash))
    backtest.PlotTradeChart(Data[TrDataSize:]) 
    #print(ValidateResult)
    
    total_result = {strPredictVal:ValidateResult[0][strPredictVal], strPredictProbVal:ValidateResult[0][strPredictProbVal], strAnsVal:ValidateResult[0][strAnsVal]}
    for index in range(1, len(ValidateResult)):
        total_result[strPredictVal] = numpy.concatenate((total_result[strPredictVal], ValidateResult[index][strPredictVal]), axis=0)
        total_result[strPredictProbVal] = numpy.concatenate((total_result[strPredictProbVal], ValidateResult[index][strPredictProbVal]), axis=0)
        total_result[strAnsVal] = numpy.concatenate((total_result[strAnsVal], ValidateResult[index][strAnsVal]), axis=0)
    
    #print(total_result)
    
    ShowSensitivitySpecificityForMultiLabels(total_result[strAnsVal], total_result[strPredictVal], total_result[strPredictProbVal], [1, 0, -1])

def ForwardingLeaveOneOutRandom(Data, Target, TrDataSize):
    
    OriginalCash = 50000
    perShareSize = 100
    RandomCount = 1000
        
    TotalProfit = 0    
    for r_count in range(RandomCount):
        random.seed(r_count)
        
        backtestParam = {BacktestParam.strStrategyParams: 
                         {BacktestParam.strBuyStrategy: BacktestParam.BuyFixed
                          , BacktestParam.strSellStrategy: BacktestParam.SellAll
                          , BacktestParam.perShareSize: perShareSize}}
        backtest = Backtest(OriginalCash, False, backtestParam)

        TsLength = len(Data.index) - TrDataSize
        for i in range(TsLength):
    
            r = random.randint(0,99) 
            if r >= 98:
                date = Data.iloc[TrDataSize+i].name
                close = Data.iloc[TrDataSize+i][strClose]
                high = Data.iloc[TrDataSize+i][strHigh]
                low = Data.iloc[TrDataSize+i][strLow]
                params = {strDate: date, strClose: close, strHigh: high, strLow: low}
            
                backtest.RunStrategy(BacktestParam.BuySignal, BacktestParam.EasyStrategy, params) 
            elif r < 2:
                date = Data.iloc[TrDataSize+i].name
                close = Data.iloc[TrDataSize+i][strClose]
                high = Data.iloc[TrDataSize+i][strHigh]
                low = Data.iloc[TrDataSize+i][strLow]
                params = {strDate: date, strClose: close, strHigh: high, strLow: low}
                
                backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params)
        
        backtest.RunStrategy(BacktestParam.SellSignal, BacktestParam.EasyStrategy, params) 
        
        FinalCash = backtest.Cash
        Profit = FinalCash - OriginalCash
        TotalProfit += Profit
        print("Profit_{0}: {1}".format(r_count, Profit)) 
    
    print("AvgProfit: {0}".format(TotalProfit/RandomCount)) 
    print("ROI: {:.2%}".format(TotalProfit/RandomCount/OriginalCash))


def RunValidation(Data, Target, type, param):
    
    if ValidationType.ForwardingLeaveOneOut == type:
        ForwardingLeaveOneOutValidation(Data, Target, param[ValidationType.TrDataSize])
    elif ValidationType.ForwardingLeaveOneOutRandom == type:
        ForwardingLeaveOneOutRandom(Data, Target, param[ValidationType.TrDataSize])

class ValidationType(Enum):
    ForwardingLeaveOneOut = 1
    ForwardingLeaveOneOutRandom = 999
    
    # ForwardingLeaveOneOut params
    TrDataSize = 'TrDataSize'