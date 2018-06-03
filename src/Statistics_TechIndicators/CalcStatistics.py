import math
from sklearn import metrics


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
