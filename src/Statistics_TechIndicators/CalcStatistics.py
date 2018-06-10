import math
from sklearn import metrics
from sklearn.metrics import roc_curve, auc


def ShowSensitivitySpecificity(AnsVal, PredictVal):

    print(metrics.confusion_matrix(AnsVal, PredictVal))

    TN, FP, FN, TP = metrics.confusion_matrix(AnsVal, PredictVal).ravel()
    
    TPR = TP/(TP+FN)
    FPR = FP/(FP+TN)
    PPV = TP/(TP+FP)
    ACC = (TP+TN)/(TP+FP+FN+TN)
    Fscore = 2*TP/(2*TP+FP+FN)
    MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
    AUC = metrics.roc_auc_score(AnsVal, PredictVal)
    
    print('TP    FP    FN    TN        TPR    FPR    PPV    ACC    Fscore    MCC    AUC\n')
    print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(TP, FP, FN, TN, TPR, FPR, PPV, ACC, Fscore, MCC, AUC))


def ShowSensitivitySpecificityForMultiLabels(AnsVal, PredictVal, PredictProbVal, LabelList):

    #print(metrics.confusion_matrix(AnsVal.argmax(axis=1), PredictVal.argmax(axis=1)))
    
    #print(*PredictProbVal, sep='\n')
    #print(*PredictVal, sep='\n')
    
    fprDict = dict()
    tprDict = dict()
    roc_aucDict = dict()
    
    for label_index in range(len(LabelList)):
        
        print(metrics.confusion_matrix(AnsVal[:,label_index], PredictVal[:,label_index]))
        
        TN, FP, FN, TP = 0, 0, 0, 0
        for index in range(len(AnsVal)):
            if AnsVal[index][label_index] == PredictVal[index][label_index]:
                if AnsVal[index][label_index] == 1:
                    TP += 1
                else:    
                    TN += 1
            elif PredictVal[index][label_index] == 1:
                FP += 1
            else:
                FN += 1
        
        if TP+FN != 0:
            TPR = TP/(TP+FN)
        else:
            TPR = float('nan')
        
        if FP+TN != 0:            
            FPR = FP/(FP+TN)
        else:
            FPR = float('nan')     

        if TP+FP != 0:
            PPV = TP/(TP+FP)
        else:
            PPV = float('nan')     
              
        ACC = (TP+TN)/(TP+FP+FN+TN)
        
        if TP+FP+FN != 0:
            Fscore = 2*TP/(2*TP+FP+FN)
        else:
            Fscore = float('nan')     

        if (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) != 0:
            MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        else:
            MCC = float('nan')                          

        # Calc AUC
        fprDict[label_index], tprDict[label_index], _ = roc_curve(AnsVal[:, label_index], PredictProbVal[:, label_index])
        roc_aucDict[label_index] = auc(fprDict[label_index], tprDict[label_index])
        
        print('Label: {0}'.format(str(LabelList[label_index]))) 
        print('    TP     FP     FN     TN   TPR    FPR    PPV    ACC    Fscore    MCC    AUC')
        print("{0:6d},{1:6d},{2:6d},{3:6d}, {4:.3f}, {5:.3f}, {6:.3f}, {7:.3f}, {8:.3f}, {9:.3f}, {10:.3f}\n".format(TP, FP, FN, TN, TPR, FPR, PPV, ACC, Fscore, MCC, roc_aucDict[label_index]))
